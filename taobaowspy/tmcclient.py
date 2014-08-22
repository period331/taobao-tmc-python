#coding: utf-8

import time
import logging
from hashlib import md5

from event import Event
from tornadowebsocket import WebSocket

logger = logging.getLogger(__name__)


class TmcClient(WebSocket, Event):
    def __init__(self, url, app_key, app_secret):
        assert isinstance(url, (str, unicode)) and len(url) > 0
        assert isinstance(app_key, (str, unicode)) and len(app_key) > 0
        assert isinstance(app_secret, (str, unicode)) and len(app_secret) > 0

        self.url = url
        self.app_secret = app_secret
        self.app_key = app_key

    def connect(self):

        self.stream.connect((self.host, self.port), self._on_connect)def 

    def on_open(self):
        pass

    def on_message(self, data):
        pass

    def on_ping(self):
        pass

    def on_pong(self):
        pass

    def on_close(self):
        pass

    def on_unsupported(self):
        pass
