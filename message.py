# coding: utf-8

from messagetype import MessageType
from struct import calcsize, unpack_from, pack
from binascii import *
from datetime import datetime
import types


class MessageIO(object):
    def __init__(self):
        pass

    def writeMessage(self, message):

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
                self.writeCustomHeader(stream, key, value)

        stream.int16(MessageType.HeaderType.endOfHeaders)

        return stream

    def writeCustomHeader(self, stream, key, value):
        stream.int16(MessageType.HeaderType.custom)
        stream.string(key)
        self.writeCustomValue(stream, value)

    def writeCustomValue(self, stream, value):
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

    def readMessage(self, bmessage):
        """ 读取消息数据 """

        def unpack_from_wrap(fmt, offset):
            return unpack_from('<' + fmt, bmessage, offset)

        message = Message(protocolVersion=unpack_from_wrap('B', 0)[0],
            messageType=unpack_from_wrap('B', calcsize('<B'))[0])

        headerType = unpack_from_wrap('H', calcsize('<2B'))[0]

        message.update_offset(calcsize('<2BH'))

        HeaderType = MessageType.HeaderType

        while headerType != HeaderType.endOfHeaders:
            if headerType ==  HeaderType.custom:
                key, message.offset = self.readCountedString(bmessage, message.offset)

                value, message.offset = self.readCustomValue(bmessage, message.offset)

                message.content[key] = value
            elif headerType == HeaderType.statusCode:
                message.statusCode = unpack_from_wrap('I', message.offset)[0]
                message.update_offset(calcsize('<I'))
            elif headerType == HeaderType.statusPhrase:
                message.statusCode, message.offset = self.readCountedString(bmessage, message.offset)
            elif headerType == HeaderType.flag:
                message.flag = unpack_from_wrap('I', message.offset)[0]
                message.update_offset(calcsize('<I'))
            elif headerType == HeaderType.token:
                message.token, message.offset = self.readCountedString(bmessage, message.offset)

            headerType = unpack_from_wrap('H', message.offset)[0]
            message.update_offset(calcsize('<H'))

        return message

    def readCountedString(self, bmessage, offset):
        """ 读取字符串 """
        length = unpack_from('<B', bmessage, offset)[0]

        if length > 0:

            s = unpack_from('<%ds' % length, bmessage, offset + calcsize('<I'))[0]

            return s.decode('utf-8'), offset + calcsize('<I%ds' % length)
        else:
            return None, offset + calcsize('<I')

    def readCustomValue(self, bmessage, offset):
        """ 读取用户数据value """
        _type = unpack_from('<B', bmessage, offset)[0]

        ValueFormat = MessageType.ValueFormat

        offset += calcsize('<B')

        if _type == ValueFormat.void:
            return None, offset
        elif _type == ValueFormat.byte:
            return unpack_from('<B', bmessage, offset)[0], offset + calcsize('<B')
        elif _type == ValueFormat.int16:
            return unpack_from('<H', bmessage, offset)[0], offset + calcsize('<H')
        elif _type == ValueFormat.int32:
            return unpack_from('<I', bmessage, offset)[0], offset + calcsize('<I')
        elif _type == ValueFormat.int64:
            return unpack_from('<Q', bmessage, offset)[0], offset + calcsize('<Q')
        elif _type == ValueFormat.date:
            ticks = unpack_from('<Q', bmessage, offset)[0]
            return datetime.fromtimestamp(float(ticks) / 1000).strftime('%Y-%m-%d %H:%M:%S'), offset + calcsize('<Q')
        elif _type == ValueFormat.byteArray:
            _l = unpack_from('<I', bmessage, offset)[0]
            return unpack_from('<%dB' % _l, bmessage, offset + calcsize('<I'))[0], offset + calcsize('<I%dB' % _l)
        else:
            return self.readCountedString(bmessage, offset);

messageIO = MessageIO()


class Message(object):
    def __init__(self, protocolVersion=2, messageType=None, statusCode=None,
                statusPhrase=None, flag=None, token=None, content={}):
        self.protocolVersion = protocolVersion
        self.messageType = messageType
        self.statusCode = statusCode
        self.statusPhrase = statusPhrase
        self.flag = flag
        self.token = token
        self.content = content if content is not None else {}

        self.offset = 0

    def update_offset(self, offset):
        self.offset = self.offset + offset

    def update_content(self, _dict):
        if isinstance(_dict, dict):
            self.content.update(_dict)

    def __str__(self):
        return '{"' + """content: "{content}", \
messageType: "{messageType}", \
statusCode: "{statusCode}", \
statusPhrase: "{statusPhrase}", \
flag: "{flag}", \
token: "{token}", \
protocolVersion: "{protocolVersion}""".format(**self.__dict__) + '"}'

    __repr__ = __str__


class ConfirmMessage(Message):
    def __init__(self, *args, **kwargs):
        super(ConfirmMessage, self).__init__(*args, **kwargs)

        self.messageType = 2

        self.content = {'__kind': 2}


class QueryMessage(Message):
    def __init__(self, *args, **kwargs):
        super(QueryMessage, self).__init__(*args, **kwargs)

        self.messageType = 2

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
