# coding: utf-8

import struct
from binascii import *
b = '020104000100000005002400000033346563376666632d666235362d343432612d626433392d6535356237333030356536640000'

# a = '02 01 0400 01000000 0500 24000000 33346563376666632d666235362d343432612d626433392d653535623733303035653664 0000'
a = '33346563376666632d666235362d343432612d626433392d653535623733303035653664'  # 72


querenlianjie = '020104000100000005002400000035346537386461382d643633362d343462622d623066652d3831396164323238343739330000'



bs = unhexlify(querenlianjie)

print len(bs)
print len(querenlianjie)

# b = Buffer(unhexlify(querenlianjie_))
# print b.read_int()

print struct.unpack('<2Bhihi36sh', bs)
print len(''.join([str(i) for i in struct.unpack('<2Bhihi36sh', bs)]))

from taobaowspy.message import _MessageIO

io = _MessageIO()
message = io.read(bs)
print message.protocol_version
print message.message_type
print message.token