# coding: utf-8


class MessageType(object):
    CONNECT = 0
    CONNECTACK = 1
    SEND = 2
    SENDACK = 3

    class HeaderType(object):
        endOfHeaders = 0
        custom = 1
        statusCode = 2
        statusPhrase = 3
        flag = 4
        token = 5

    class ValueFormat(object):
        void = 0
        countedString = 1
        byte = 2
        int16 = 3
        int32 = 4
        int64 = 5
        date = 6
        byteArray = 7
