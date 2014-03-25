# coding: utf8

from Queue import Queue
from random import randint
import time

from client import TaobaoClient
from utils import Shop, get_logger
from taobaowsclient import TaobaoWsClient
from threads import TaobaoWsThread, HeartbeatThread, InitiativeQuery


class MessageManager(object):

    _ws_url = 'ws://mc.api.taobao.com/'

    def __init__(self, **kwargs):
        self.connections = kwargs.pop('connections', 4)  # 连接数

        self.client = TaobaoClient(**kwargs)
        self.ws_clients = []

        self._ws_url = kwargs.pop('ws_url', MessageManager._ws_url)
        self.appkey = kwargs.pop('appkey', '')
        self.secret = kwargs.pop('secret', '')

        self.message_queue = Queue()

        self.__logger = None

        self._shops = []

    def _create_threads(self):

        def _create_client(_index):
            return TaobaoWsClient(url=self._ws_url, group_name='default', delegate=self.on_message, log=self.info,
                                  app_key=self.appkey, secret=self.secret, log_group_name='default-' + str(_index))

        for index in range(self.connections):
            _client = _create_client(index)
            self.ws_clients.append(_client)
            _thread = TaobaoWsThread(_client)
            _thread.setDaemon(True)
            _thread.start()

            time.sleep(1)

        heartbeat = HeartbeatThread(self.ws_clients, log=self.info)
        heartbeat.setDaemon(True)
        heartbeat.start()

    def _get_alive_client(self):
        """ 获得一个活动的线程 """
        def _():
            _randint = randint(0, len(self.ws_clients) - 1)

            _client = self.ws_clients[_randint]

            if _client.sock is not None and _client.keep_running:
                return _client
            else:
                return _()

        return _()

    def on_message(self, message):
        self.message_queue.put_nowait(message)

    def set_shops(self, shops):

        if not isinstance(shops, list):
            shops = [shops]

        for shop in shops:
            if isinstance(shop, Shop):
                self._shops.append(shop)

    def info(self, msg):
        """ 记录日志 """

        self.__get_logger().info(msg)

    def __get_logger(self):
        """ 获得日志记录对象 """
        if self.__logger is None:

            self.__logger = get_logger(__name__)

        return self.__logger

    def run(self):
        """ 开启运行 """

        # with InitiativeQuery(self._get_alive_client, self.info) as iq:

        self._create_threads()

        while True:
            message = self.message_queue.get()

            # if message is not None:
            #     iq.reset_frequency()

            _client = self._get_alive_client()

            _client.send_confirm(message['id'])

            print message


if __name__ == '__main__':

    _shop = Shop(name='sandbox_c_1', session='6100f19de277a4d7dd68fafd0991b2b912c3294f50fa1e02074082786')

    manager = MessageManager(connections=3, appkey='', secret='',
                             url='http://gw.api.tbsandbox.com/router/rest',
                             session='6100f19de277a4d7dd68fafd0991b2b912c3294f50fa1e02074082786',
                             ws_url='ws://mc.api.tbsandbox.com/')

    manager.set_shops([_shop])

    manager.run()
