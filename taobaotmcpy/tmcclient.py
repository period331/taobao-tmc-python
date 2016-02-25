# coding: utf-8
__author__ = 'baocaixiong'

import time
import logging
from hashlib import md5

from tornado import ioloop

from event import Event
from message import Message
from messageio import reader, writer
from tornadowebsocket import WebSocket
from utils import confirm_message, query_message

logger = logging.getLogger('taobao-tmc')


class TmcClient(WebSocket, Event):
    def __init__(self, url, app_key, app_secret, group_name='default', query_message_interval=50, heartbeat_interval=30,
                 sdk_version='top-sdk-java-201403304', *args, **kwargs):
        super(TmcClient, self).__init__(url, *args, **kwargs)
        Event.__init__(self)

        self.on('on_init', lambda: logger.info('WebSocket Start Connect: %s@%s' % (url, group_name)))

        assert isinstance(url, (str, unicode)) and len(url) > 0
        assert isinstance(app_key, (str, unicode)) and len(app_key) > 0
        assert isinstance(app_secret, (str, unicode)) and len(app_secret) > 0
        assert isinstance(group_name, (str, unicode)) and len(group_name) > 0
        assert isinstance(query_message_interval, int) and 0 < query_message_interval < 60
        assert isinstance(heartbeat_interval, int) and 0 < heartbeat_interval < 60

        self.sdk_version = sdk_version
        self.url = url
        self.app_secret = app_secret
        self.app_key = app_key
        self.group_name = group_name
        self.query_message_interval = query_message_interval
        self.heartbeat_interval = heartbeat_interval

        self.token = None

        self.fire('on_init')
        self.on('on_handshake_success', self._start_query_loop)
        self.on('on_confirm_message', self._on_confirm_message)

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
        logger.info('TMC Handshake Start.')

        params = {
            'timestamp': str(timestamp),
            'app_key': self.app_key,
            'sdk': self.sdk_version,
            'sign': self.create_sign(timestamp),
            'group_name': self.group_name,
        }

        message = writer(Message(2, 0, flag=1, content=params))

        self.write_binary(message)

        self.fire('on_open')

    def write_binary(self, message):
        self.write_message(message, True)

    def on_message(self, data):
        try:
            message = reader(data)
        except:
            logging.error('[%s]Message Parse Error.' % self.group_name)
            self.fire('parse_message_error')
            raise

        self.fire('received_message')
        logger.debug('[%s]Received Message %s' % (self.group_name, message))

        if message.message_type == 1:  # 发送连接数据返回
            self.token = message.token
            if self.token:
                logger.info('[%s]TMC Handshake Success. The Token Is %s' % (self.group_name, message.token))
                self.fire('on_handshake_success', token=self.token)
            else:
                logging.info('[%s]TMS Handshake Failed, Token Is Empty, Error: %s' % (self.group_name, message))

        elif message.message_type == 2:  # 服务器主动通知消息
            self.fire('on_confirm_message', message_id=message.content.get('id'))
            self.fire('on_message', message=message)
        elif message.message_type == 3:  # 主动拉取消息返回
            print data

    def on_ping(self):
        logger.debug('[%s]Received Ping.' % self.group_name)
        self.fire('on_ping')

    def on_pong(self):
        logger.debug('[%s]Received Pong.' % self.group_name)
        self.fire('on_pong')

    def on_close(self):
        logger.error('[%s]TMC Connection Close Error.' % self.group_name)
        self.fire('on_close')

    def on_unsupported(self):
        self.fire('on_abort')
        logger.error('[%s]Abort Error.' % self.group_name)

    def _on_confirm_message(self, message_id):
        cm = confirm_message(message_id, self.token)
        logger.debug('[%s]Confirm Message: %s' % (self.group_name, message_id))
        self.write_binary(cm)

    def _start_query_loop(self):
        """ 开启主动拉取消息循环 """

        def _query_message_loop(_self, group_name, _token):
            def _():
                logger.debug('[%s]Send Query Message Request.' % group_name)
                _self.write_binary(query_message(token=_token))

            return _

        periodic = ioloop.PeriodicCallback(_query_message_loop(self, self.group_name, self.token),
                                           self.query_message_interval * 1000, io_loop=self.io_loop)

        logger.info('[%s]Start Query Message Interval.' % self.group_name)

        periodic.start()

