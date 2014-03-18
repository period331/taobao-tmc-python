# coding: utf-8

import sys
import time
import struct
import bitstring
import threading

from binascii import *

from utils import createSign

sys.path.insert(0, '/Users/baocaixiong/ProgramFiles/websocket-client')

from websocket import create_connection, enableTrace

# enableTrace(True)

import struct

from message import MessageIO, Message

messageIo = MessageIO()

conn = create_connection('ws://mc.api.taobao.com/')
# conn = create_connection('ws://127.0.0.1:10000')

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

message = Message(2, 0, flag=1, content=request)
stream = messageIo.writeMessage(message)

_queryMessage = Message(2, 2, content={'__kind': str(1)})

confirmMessage = Message(2, 2, content={"__kind": str(2)})

# print b2a_hex(stream)
# print stream

def _send_ping(token):
    while 1:
        _queryMessage.token = token
        m = messageIo.writeMessage(_queryMessage)

        print m, '=============string'

        print b2a_hex(m)
        conn.send_binary(m)
        time.sleep(1)

_ = 0

_queryMessageThread = False

print conn.send_binary(stream)
while 1:

    result =  conn.recv()

    print b2a_hex(result)

    message = messageIo.readMessage(result)

    if not _queryMessageThread:
        thread = threading.Thread(target=_send_ping, args=(message.token,))
        thread.setDaemon(True)
        thread.start()

        _queryMessageThread = True

    print message.token, message.messageType, message.statusCode, message.statusPhrase, 'gahahahah'
    print message.content


    time.sleep(0.5)

conn.close()