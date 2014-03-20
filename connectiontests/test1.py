# coding: utf-8

import sys
import time

import bitstring
from taobaowspy.utils import gen_sign


sys.path.insert(0, '/Users/baocaixiong/ProgramFiles/websocket-client')

from websocket import create_connection, enableTrace

enableTrace(True)

import struct


class DataStream(bytearray):

    def append(self, v, fmt='>B'):

        if type(v) is str:
            self.extend(struct.pack(fmt, len(v)))
            self.extend(struct.pack("I%ds" % (len(v),), len(v), v))
        else:
            self.extend(struct.pack(fmt, v))

conn = create_connection('ws://mc.api.tbsandbox.com/')
# conn = create_connection('ws://127.0.0.1:10000')

app_key = '1021737885'
group_name = 'default'
secret = 'sandboxbbf5579605d7936422c11af0e'
timestamp = int(round(time.time() * 1000))

request = {
    'app_key': app_key,
    'group_name': group_name,
    'timestamp': timestamp
}

sign = gen_sign(app_key, group_name, secret, timestamp)

# stream = DataStream();
# stream.append(2)
# stream.append(0)

# stream.append(1)
# stream.append('app_key')
# stream.append(app_key)


# stream.append(1)
# stream.append('group_name')
# stream.append(group_name)


# stream.append(1)
# stream.append('timestamp')
# stream.append('%s' % timestamp)

# stream.append(1)
# stream.append('sign')
# stream.append(sign)

# stream.append(0)


# request['sdk'] = 'sdk'

stream = bitstring.BitStream()
stream.append('int:8=2')
stream.append('int:8=0')
stream.append('int:16=4')
stream.append('int:16=1')

stream.append('int:16=1')

print conn.send_binary(stream)

# # conn.send(chr(0x02) + chr(0x00) + chr(0x0004)+chr(0x00000001)+chr(0x0000))
# print "Sent"
# print "Reeiving..."
result = conn.recv()
print "Received '%s'" % result
conn.close()