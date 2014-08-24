# coding: utf-8

__all__ = ['ConfirmMessage', 'QueryMessage', 'Message']

from struct import calcsize, unpack_from, pack
from datetime import datetime
import types
from json import dumps


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
        return dumps(self.__dict__, ensure_ascii=False)

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
