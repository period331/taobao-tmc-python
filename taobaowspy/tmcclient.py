#coding: utf-8

import time
import logging
from hashlib import md5

from event import Event
from tornadowebsocket import WebSocket
from message import reader, writer, Message
from tornado import ioloop, iostream

logger = logging.getLogger(__name__)


class TmcClient(WebSocket, Event):
    def __init__(self, url, app_key, app_secret, group_name='default', *args, **kwargs):
        super(TmcClient, self).__init__(url, *args, **kwargs)

        assert isinstance(url, (str, unicode)) and len(url) > 0
        assert isinstance(app_key, (str, unicode)) and len(app_key) > 0
        assert isinstance(app_secret, (str, unicode)) and len(app_secret) > 0
        assert isinstance(group_name, (str, unicode)) and len(group_name) > 0

        self.url = url
        self.app_secret = app_secret
        self.app_key = app_key
        self.group_name = group_name

    def create_sign(self, timestamp):
        timestamp = timestamp if timestamp else int(round(time.time() * 1000))
        params = {
            'group_name': self.group_name,
            'app_key': self.app_key,
            'timestamp': timestamp,
        }

        keys = params.keys()
        keys.sort()
        
        params = "%s%s%s" % (self.app_secret, str().join('%s%s' % (key, params[key]) for key in keys), self.app_secret)
        return md5(params).hexdigest().upper()

    def on_open(self):
        timestamp = int(round(time.time() * 1000))

        params = {
            'timestamp': str(timestamp),
            'app_key': self.app_key,
            'sdk': 'top-sdk-java-201403304',
            'sign': self.create_sign(timestamp),
            'group_name': self.group_name,
        }

        message = writer(Message(2, 0, flag=1, content=params))

        self.write_binary(message)

    def write_binary(self, message):
        self.write_message(message, True)

    def on_message(self, data):
        message = reader(data)
        print message

    def on_ping(self):
        print 'on_ping'

    def on_pong(self):
        print 'on_pong'

    def on_close(self):
        print 'on_close'

    def on_unsupported(self):
        print 'on_unsupported'


if __name__ == '__main__':
    ws = TmcClient('ws://mc.api.tbsandbox.com/', '1021737885', 'sandboxbbf5579605d7936422c11af0e', 'default')
    try:
        ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        pass
    finally:
        ws.close()
