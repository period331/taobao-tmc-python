# coding: utf8


class MessageManager(object):
    def __init__(self, **kwargs):
        self.connections = kwargs.pop('connections', 4)  # 连接数
        self.url = kwargs.pop('url', None)  # 连接地址