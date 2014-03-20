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

app_key = '1021737885'
group_name = 'default'
secret = 'sandboxbbf5579605d7936422c11af0e'
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

socket = WebSocket('ws://mc.api.tbsandbox.com/', onmessage=my_msg_handler)
socket.onopen = lambda: socket.send(stream)

try:
  asyncore.loop()
except KeyboardInterrupt:
  socket.close()