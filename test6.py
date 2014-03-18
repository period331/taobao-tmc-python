# coding: utf-8

import sys, asyncore

sys.path.insert(0, '/Users/baocaixiong/PythonProjects/python-websocket')

import time
import struct
from websocket import WebSocket

from binascii import *

from utils import createSign

from message import MessageIO, Message

messageIo = MessageIO()

conn = WebSocket('ws://mc.api.taobao.com/')
# conn = create_connection('ws://127.0.0.1:10000')

app_key = ''
group_name = 'default'
secret = ''
timestamp = int(round(time.time() * 1000))



request = {
    'timestamp' : str(timestamp),
    'app_key' : app_key,
    'sdk': 'top-sdk-java-201403304',
    'sign': createSign(app_key, group_name, secret, timestamp),
    'group_name' : group_name,
}



def my_msg_handler(msg):
    message = messageIo.readMessage(result)

    print message.content

message = Message(2, 0, flag=1, content=request)
stream = messageIo.writeMessage(message)

socket = WebSocket('ws://mc.api.taobao.com/', onmessage=my_msg_handler)
socket.onopen = lambda: socket.send(stream)

try:
  asyncore.loop()
except KeyboardInterrupt:
  socket.close()