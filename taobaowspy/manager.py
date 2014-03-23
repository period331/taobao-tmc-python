# coding: utf8

from Queue import Queue
from client import TaobaoClient
from utils import Shop, get_logger
from taobaowsclient import TaobaoWsClient
from threads import TaobaoWsThread, HeartbeatThread


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

        heartbeat = HeartbeatThread(self.ws_clients, log=self.info)
        heartbeat.setDaemon(True)
        heartbeat.start()

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


if __name__ == '__main__':

    _shop = Shop(name='sandbox_c_1', session='61005236cadbd3f41c8aea2d4ba802017c0c448d3f487ac2074082786')

    manager = MessageManager(connections=3, appkey='1021737885', secret='sandboxbbf5579605d7936422c11af0e',
                             url='http://gw.api.tbsandbox.com/router/rest',
                             session='6100f11de277a4d7dd6153772368fafd0993294f50fa1e02074082786',
                             ws_url='ws://mc.api.tbsandbox.com/')

    manager.set_shops([_shop])
