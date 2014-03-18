# coding: utf-8

import sys
import time
import struct
from binascii import *
from buffer import Buffer
b = '020104000100000005002400000033346563376666632d666235362d343432612d626433392d6535356237333030356536640000'

# a = '02 01 0400 01000000 0500 24000000 33346563376666632d666235362d343432612d626433392d653535623733303035653664 0000'
a = '33346563376666632d666235362d343432612d626433392d653535623733303035653664'  # 72


querenlianjie_ = '020104000100000005002400000035346537386461382d643633362d343462622d623066652d3831396164323238343739330000'

querenlianjie = '8234020104000100000005002400000034316265306431352d383436322d346431652d623265312d3866376232353935383663350000'



bs = unhexlify(querenlianjie)

print len(bs)
print len(querenlianjie)

# b = Buffer(unhexlify(querenlianjie_))
# print b.read_int()

print struct.unpack('<2Bhihi36sh', bs)
print len(''.join([str(i) for i in struct.unpack('<2Bhihi36sh', bs)]))

from message import MessageIO

io = MessageIO()
message = io.readMessage(bs)
print message.protocolVersion
print message.messageType
print message.token