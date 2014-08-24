# coding: utf8

from random import randint
from Queue import Queue
import time
import logging

from taobaotmcpy.client import TaobaoClient
from taobaotmcpy.shop import Shop
from taobaotmcpy.tmcclient import TmcClient

from tornado import ioloop

logger = logging.getLogger(__name__)


class MessageManager(object):

    _ws_url = 'ws://mc.api.taobao.com/'

    def __init__(self, **kwargs):
        self.connections = kwargs.pop('connections', 4)  # 连接数
        self._ws_url = kwargs.pop('ws_url', self._ws_url)
        self.appkey = kwargs.pop('appkey', '')
        self.secret = kwargs.pop('secret', '')

        assert self.connections > 1
        assert isinstance(self._ws_url, basestring) and len(self._ws_url) > 0
        assert isinstance(self.appkey, basestring) and len(self._ws_url) > 0
        assert isinstance(self.secret, basestring) and len(self._ws_url) > 0

        self.client = TaobaoClient(**kwargs)
        self.ws_clients = []

        self.queue = Queue()

        self._shops = []

    def connecte(self):

        def _create_client(_index):
            return TmcClient(url=self._ws_url, group_name='default', app_key=self.appkey, secret=self.secret)

        for index in range(self.connections):
            _client = _create_client(index)
            _client.on('on_message', self.on_message)
            self.ws_clients.append(_client)

    def on_message(self, message=message):
        self.message_queue.put_nowait(message)

    def set_shops(self, shops):

        if not isinstance(shops, list):
            shops = [shops]

        for shop in shops:
            if isinstance(shop, Shop):
                self._shops.append(shop)

    def run(self):
        while 1:
            message = self.message_queue.get()

            print message


if __name__ == '__main__':

    _shop = Shop(name='sandbox_c_1', session='6100f19de277a4d7dd68fafd0991b2b912c3294f50fa1e02074082786')

    manager = MessageManager(connections=3, appkey='', secret='',
                             url='http://gw.api.tbsandbox.com/router/rest',
                             session='6100f19de277a4d7dd68fafd0991b2b912c3294f50fa1e02074082786',
                             ws_url='ws://mc.api.tbsandbox.com/')

    manager.set_shops([_shop])

    manager.run()
