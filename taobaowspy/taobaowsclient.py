# coding: utf8

import time
import traceback
import sys
from websocket import ABNF, WebSocketConnectionClosedException, default_timeout, WebSocket, WebSocketException
from hashlib import md5

from message import messageIO, ConfirmMessage, Message
from messagetype import MessageType


class TaobaoWsClient(object):
    def __init__(self, url, group_name='', app_key='', secret='', delegate=None, log=None, log_group_name=None):
        self.on_message = delegate if callable(delegate) else lambda message: None
        self.log = log if callable(log) else lambda msg: None

        self.url = url
        self.group_name = group_name
        self.app_key = app_key
        self.secret = secret

        self.log_group_name = log_group_name if log_group_name is not None \
            else '%s-%s' % (self.group_name, id(self))

        self.sock = None
        self.keep_running = False
        self.delegate = None

        self.token = None

    def send(self, data, opcode=ABNF.OPCODE_TEXT):
        if self.sock.send(data, opcode) == 0:
            raise WebSocketConnectionClosedException()

    def send_binary(self, payload):
        """ 发送二进制数据 """

        self.send(payload, opcode=ABNF.OPCODE_BINARY)

    def send_confirm(self, message_id):

        cm = ConfirmMessage()
        cm.token = self.token
        cm.update_content({'id': message_id})

        self.log('连接: %s, 确认消息数据: %s' % (self.log_group_name, message_id))

        self.send_binary(messageIO.writeMessage(cm))

    def ping(self):
        if self.sock:
            # self.log('连接: %s 开始ping服务器' % self.log_group_name)
            self.sock.ping()

    @staticmethod
    def on_error(self, *args):
        """ 记录错误 """
        self.keep_running = False
        exc_type, exc_val, exc_tb = args
        exc = str(traceback.extract_tb(exc_tb))

        msg = '连接: %s 消息服务出现异常, %s exception:%s, trace:%s' % (
            self.log_group_name, exc_val, exc_type.__name__, exc)

        self.log(msg)

        self._restart()

    @staticmethod
    def on_message(self, message):
        """ 当接受到消息时 """

        m_types = {
            str(MessageType.SEND): '接收',
            str(MessageType.SENDACK): '响应'
        }

        self.log('连接: %s %s到消息: %s' % (
            self.log_group_name, m_types.get(str(message.messageType), ''), message)
        )

        if len(message.content) > 0 and str(message.messageType) in m_types.keys():
            self.delegate(message.content)

    @staticmethod
    def on_close(self):
        """ 链接关闭时 """

        self.keep_running = False

        self._restart()

    @staticmethod
    def on_open(self):
        """ 连接打开时 """

        timestamp = int(round(time.time() * 1000))

        params = {
            'timestamp': str(timestamp),
            'app_key': self.app_key,
            'sdk': 'top-sdk-java-201403304',
            'sign': self.create_sign(timestamp),
            'group_name': self.group_name,
        }

        message = messageIO.writeMessage(Message(2, 0, flag=1, content=params))

        self.send_binary(message)

    def _restart(self):
        """ 重启线程 """

        self.log('连接: %s 10秒之后重启连接' % self.group_name)
        time.sleep(10)

        self.sock = None
        self.keep_running = True

        self.run_forever()

    def create_sign(self, timestamp):
        timestamp = timestamp if timestamp else int(round(time.time() * 1000))
        params = {
            'group_name': self.group_name,
            'app_key': self.app_key,
            'timestamp': timestamp,
        }

        param_list = sorted(params.iteritems(), key=lambda d: d[0], reverse=False)

        param_str = self.secret

        for (key, value) in param_list:
            param_str = param_str + key + str(value)

        param_str += self.secret

        return md5(param_str).hexdigest().upper()

    def run_forever(self, sockopt=None, sslopt=None):
        """ 运行 """

        sockopt = sockopt if sockopt else []
        sslopt = sslopt if sslopt else {}

        if self.sock:
            raise WebSocketException("socket is already opened")

        try:
            self.sock = WebSocket(sockopt=sockopt, sslopt=sslopt)
            self.sock.settimeout(default_timeout)
            self.sock.connect(self.url, header={})
            self._callback(self.on_open)

            conn_message = self.sock.recv()

            try:
                message = messageIO.readMessage(conn_message)
            except:
                message = Message()

            if message.token:
                self.log('连接: %s 连接成功, token: %s' % (self.log_group_name, message.token))

                self.token = message.token
            else:
                raise Exception(
                    '连接: %s 连接失败, 原因: %s %s' % (
                        self.log_group_name, message.status_code, message.status_phrase
                    ))

            while self.keep_running:
                data = self.sock.recv()

                try:
                    if data is None:
                        continue

                    message = messageIO.readMessage(data)

                    self._callback(self.on_message, message)
                except:
                    continue
        except:
            self._callback(self.on_error, *sys.exc_info())
        finally:
            self.sock.close()
            self._callback(self.on_close)
            self.sock = None

    def _callback(self, callback, *args):
        if callback:
            try:
                callback(self, *args)
            except:
                self.on_error(self, *sys.exc_info())
