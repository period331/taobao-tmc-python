# coding: utf-8

from struct import calcsize, unpack_from, pack
from datetime import datetime
import types

from taobaowspy.messagetype import MessageType


class MessageIO(object):
    def __init__(self):
        pass

    def write(self, message):

        stream = WriteBuffer()

        stream.byte(message.protocolVersion)
        stream.byte(message.messageType)

        if message.statusCode is not None:
            stream.int16(MessageType.HeaderType.statusCode)
            stream.int32(message.statusCode)

        if message.statusPhrase is not None:
            stream.int16(MessageType.HeaderType.statusCode)
            stream.string(message.statusPhrase)

        if message.flag is not None:
            stream.int16(MessageType.HeaderType.flag)
            stream.int32(message.flag)

        if message.token is not None:
            stream.int16(MessageType.HeaderType.token)
            stream.string(message.token)

        if len(message.content) > 0:
            for key, value in message.content.items():
                self.write_custom_header(stream, key, value)

        stream.int16(MessageType.HeaderType.endOfHeaders)

        return stream

    def write_custom_header(self, stream, key, value):
        stream.int16(MessageType.HeaderType.custom)
        stream.string(key)
        self.write_custom_value(stream, value)

    @staticmethod
    def write_custom_value(stream, value):
        if not value:
            stream.byte(MessageType.ValueFormat.void)

        if isinstance(value, types.IntType) and value < ((1 << 8) - 1):
            stream.byte(MessageType.ValueFormat.byte)
            stream.byte(value)
        elif isinstance(value, types.IntType) and value < ((1 << 16) - 1):
            stream.byte(MessageType.ValueFormat.int16)
            stream.int16(value)
        elif isinstance(value, types.IntType) and value < ((1 << 32) - 1):
            stream.byte(MessageType.ValueFormat.int32)
            stream.int32(value)
        elif isinstance(value, types.IntType) and value < ((1 << 64) - 1):
            stream.byte(MessageType.ValueFormat.int64)
            stream.int64(value)
        else:
            stream.byte(MessageType.ValueFormat.countedString)
            stream.string(value)

    def read(self, stream):
        """ 读取消息数据 """

        def unpack_from_wrap(fmt, offset):
            return unpack_from('<' + fmt, stream, offset)

        message = Message(protocol_version=unpack_from_wrap('B', 0)[0],
                          message_type=unpack_from_wrap('B', calcsize('<B'))[0])

        header_type = unpack_from_wrap('H', calcsize('<2B'))[0]

        message.update_offset(calcsize('<2BH'))

        _header_type = MessageType.HeaderType

        while header_type != _header_type.endOfHeaders:
            if header_type == _header_type.custom:
                key, message.offset = self.read_counted_str(stream, message.offset)

                value, message.offset = self.read_custom_value(stream, message.offset)

                message.content[key] = value
            elif header_type == _header_type.statusCode:
                message.status_code = unpack_from_wrap('I', message.offset)[0]
                message.update_offset(calcsize('<I'))
            elif header_type == _header_type.statusPhrase:
                message.status_code, message.offset = self.read_counted_str(stream, message.offset)
            elif header_type == _header_type.flag:
                message.flag = unpack_from_wrap('I', message.offset)[0]
                message.update_offset(calcsize('<I'))
            elif header_type == _header_type.token:
                message.token, message.offset = self.read_counted_str(stream, message.offset)

            header_type = unpack_from_wrap('H', message.offset)[0]
            message.update_offset(calcsize('<H'))

        return message

    @staticmethod
    def read_counted_str(stream, offset):
        """ 读取字符串 """
        length = unpack_from('<B', stream, offset)[0]

        if length > 0:

            s = unpack_from('<%ds' % length, stream, offset + calcsize('<I'))[0]

            return s.decode('utf-8'), offset + calcsize('<I%ds' % length)
        else:
            return None, offset + calcsize('<I')

    def read_custom_value(self, stream, offset):
        """ 读取用户数据value """
        _type = unpack_from('<B', stream, offset)[0]

        _value_fmt = MessageType.ValueFormat

        offset += calcsize('<B')

        if _type == _value_fmt.void:
            return None, offset
        elif _type == _value_fmt.byte:
            return unpack_from('<B', stream, offset)[0], offset + calcsize('<B')
        elif _type == _value_fmt.int16:
            return unpack_from('<H', stream, offset)[0], offset + calcsize('<H')
        elif _type == _value_fmt.int32:
            return unpack_from('<I', stream, offset)[0], offset + calcsize('<I')
        elif _type == _value_fmt.int64:
            return unpack_from('<Q', stream, offset)[0], offset + calcsize('<Q')
        elif _type == _value_fmt.date:
            ticks = unpack_from('<Q', stream, offset)[0]
            return datetime.fromtimestamp(float(ticks) / 1000).strftime('%Y-%m-%d %H:%M:%S'), offset + calcsize('<Q')
        elif _type == _value_fmt.byteArray:
            _l = unpack_from('<I', stream, offset)[0]
            return unpack_from('<%dB' % _l, stream, offset + calcsize('<I'))[0], offset + calcsize('<I%dB' % _l)
        else:
            return self.read_counted_str(stream, offset)


messageIO = MessageIO()


class Message(object):
    def __init__(self, protocol_version=2, message_type=None, status_code=None,
                 status_phrase=None, flag=None, token=None, content=None):
        self.protocol_version = protocol_version
        self.message_type = message_type
        self.status_code = status_code
        self.status_phrase = status_phrase
        self.flag = flag
        self.token = token
        self.content = content if content is not None and isinstance(content, dict) else {}

        self.offset = 0

    def update_offset(self, offset):
        self.offset = self.offset + offset

    def update_content(self, _dict):
        if isinstance(_dict, dict):
            self.content.update(_dict)

    def __str__(self):
        return '{"' + """content": "{content}", \
"message_type": "{message_type}", \
"status_code": "{status_code}", \
"status_phrase": "{status_phrase}", \
"flag": "{flag}", \
"token": "{token}", \
"protocol_version": "{protocol_version}""".format(**self.__dict__) + '"}'

    __repr__ = __str__


class ConfirmMessage(Message):
    def __init__(self, *args, **kwargs):
        super(ConfirmMessage, self).__init__(*args, **kwargs)

        self.message_type = 2

        self.content = {'__kind': 2}


class QueryMessage(Message):
    def __init__(self, *args, **kwargs):
        super(QueryMessage, self).__init__(*args, **kwargs)

        self.message_type = 2

        self.content = {'__kind': 1}


class WriteBuffer(bytearray):
    def byte(self, v):
        self.extend(pack('<B', v))

    def string(self, v):
        if len(v) > 0:
            self.extend(pack('<I%ds' % len(v), len(v), str(v)))
        else:
            self.extend(pack('<B', 0))

    def int16(self, v):
        self.extend(pack('<H', v))

    def int32(self, v):
        self.extend(pack('<I', v))

    def int64(self, v):
        self.extend(pack('<Q', v))
