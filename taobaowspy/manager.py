# coding: utf8

from Queue import Queue


class MessageManager(object):
    def __init__(self, **kwargs):
        self.connections = kwargs.pop('connections', 4)  # 连接数
        self.url = kwargs.pop('url', None)  # 连接地址

        self.appkey = kwargs.pop('appkey', '')
        self.secret = kwargs.pop('secret', '')

        self.message_queue = Queue()

    def _on_init(self):
        pass


if __name__ == '__main__':
    manager = MessageManager(connections=3, url='ws://mc.api.tbsandbox.com/',
        appkey='1021737885', secret='sandboxbbf5579605d7936422c11af0e')
