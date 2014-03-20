# coding: utf-8

import sys
import time
from utils import createSign
from binascii import *
sys.path.insert(0, '/Users/baocaixiong/PythonProjects/WebSocket-for-Python')

from ws4py.client.threadedclient import WebSocketClient

from message import MessageIO, Message

messageIo = MessageIO()

app_key = ''
group_name = 'default'
secret = ''
timestamp = int(round(time.time() * 1000))



request = {
    'timestamp' : str(timestamp),
    'app_key' : app_key,
    # 'sign': '869FA08A2D474FCDCF04D20F895DCB58',
    'sdk': 'top-sdk-java-201403304',
    'sign': createSign(app_key, group_name, secret, timestamp),
    'group_name' : group_name,
}

connMessage = Message(2, 0, flag=1, content=request)
connStream = messageIo.writeMessage(connMessage)

_queryMessage = Message(2, 2, content={'__kind': 1})

def _send_ping(token):
    while 1:
        _queryMessage.token = token
        m = messageIo.writeMessage(_queryMessage)

        print m, '=============string'

        conn.send_binary(m)
        time.sleep(1)

class DummyClient(WebSocketClient):
    def opened(self):

        self.send_binary(connStream)
        # self.send_binary()handshake_ok

        self.queryMessage = Message(2, 2, content={'__kind': 1})

    def closed(self, code, reason=None):
        print "Closed down", code, reason

    def received_message(self, m):
        message = messageIo.readMessage(m.data)


        if message.content:
            print '发送确认消息'
            confirmMessage = Message(2, 2, content={"__kind": str(2), 'id': message.content['id']})
            self.send_binary(messageIo.writeMessage(confirmMessage))

        print message.content, message.messageType, message.token

    def send_binary(self, payload):
        self.send(payload, True)


if __name__ == '__main__':
    try:
        ws = DummyClient('ws://mc.api.taobao.com/', heartbeat_freq=30)
        ws.connect()
        ws.run_forever()
    except Exception, e:
        print e
        ws.close()