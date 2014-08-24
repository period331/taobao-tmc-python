# coding: utf-8

__all__ = ['confirm_message', 'query_message', 'Message']

from struct import calcsize, unpack_from, pack
from datetime import datetime
import types

from messageio import writer, reader


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

        return self

    def update_content(self, _dict):
        if isinstance(_dict, dict):
            self.content.update(_dict)

        return self

    def __str__(self):
        return '{"' + """content": "{content}", \
"message_type": {message_type}, \
"status_code": "{status_code}", \
"status_phrase": "{status_phrase}", \
"flag": "{flag}", \
"token": "{token}", \
"protocol_version": "{protocol_version}""".format(**self.__dict__) + '"}'

    __repr__ = __str__


class _ConfirmMessage(Message):
    def __init__(self, *args, **kwargs):
        super(_ConfirmMessage, self).__init__(*args, **kwargs)

        self.message_type = 2

        self.content = {'__kind': 2}


def confirm_message(message_id, token):
    cm = _ConfirmMessage()
    cm.token = token
    cm.update_content({'id': message_id})

    return writer(cm)


class _QueryMessage(Message):
    def __init__(self, *args, **kwargs):
        super(_QueryMessage, self).__init__(*args, **kwargs)

        self.message_type = 2

        self.content = {'__kind': 1}


query_message = lambda **kwargs: writer(_QueryMessage(**kwargs))
