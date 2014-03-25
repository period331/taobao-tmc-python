# coding: utf-8

import sys
import time
import threading
from binascii import *

from taobaowspy.utils import gen_sign


sys.path.insert(0, '/Users/baocaixiong/ProgramFiles/websocket-client')

from websocket import create_connection

# enableTrace(True)

from taobaowspy.message import _MessageIO, Message

messageIo = _MessageIO()

conn = create_connection('ws://mc.api.tbsandbox.com/')
# conn = create_connection('ws://127.0.0.1:10000')

app_key = '1021737885'
group_name = 'default'
secret = 'sandboxbbf5579605d7936422c11af0e'
timestamp = int(round(time.time() * 1000))

request = {
    'timestamp': str(timestamp),
    'app_key': app_key,
    'sdk': 'top-sdk-java-201403304',
    'sign': gen_sign(app_key, group_name, secret, timestamp),
    'group_name': group_name,
}

message = Message(2, 0, flag=1, content=request)
stream = messageIo.write(message)

_queryMessage = Message(2, 2, content={'__kind': 1})

confirmMessage = Message(2, 2, content={"__kind": str(2)})

# print b2a_hex(stream)
# print stream


def _send_ping(token):
    while 1:
        _queryMessage.token = token
        m = messageIo.write(_queryMessage)

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

    message = messageIo.read(result)

    if not _queryMessageThread:
        thread = threading.Thread(target=_send_ping, args=(message.token,))
        thread.setDaemon(True)
        thread.start()

        _queryMessageThread = True

    print message.token, message.messageType, message.statusCode, message.statusPhrase, 'gahahahah'
    print message.content

    time.sleep(0.5)

conn.close()