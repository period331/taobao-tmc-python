# coding: utf-8

import struct

class Buffer(object):
    def __init__(self, bytes=None, recogn=10000):
        if (bytes == None):
            self.length = 4
            self.buffer = struct.pack('i', recogn)
        else:
            self.length = len(bytes)
            self.buffer = bytes
    
    def write_char(self, c):
        self.buffer = self.buffer + struct.pack('c', c);
        self.length = self.length + 1
        
    def write_short(self, value):    
        self.buffer = self.buffer + struct.pack('h', value);
        self.length = self.length + 2
        
    def write_int(self, value):
        self.buffer = self.buffer + struct.pack('i', value);
        self.length = self.length + 2
        
    def write_utf(self, strings):
        self.write_short(len(strings))
        self.buffer = self.buffer + struct.pack('%ds' % len(strings), strings);
        self.length = self.length + len(strings)
        
    def to_bytes(self):
        bytes = struct.pack('i', self.length + 4) + self.buffer
#        a,b = struct.unpack('ii',bytes)
        return bytes
    
    def read_char(self):
        c, self.buffer = struct.upack('c%ds' % (len(self.buffer) - 1), self.buffer)
        return c
    
    def read_short(self):
        value, self.buffer = struct.unpack('h%ds' % (len(self.buffer) - 2), self.buffer)
        return value
    
    def read_int(self):
        value, self.buffer = struct.unpack('i%ds' % (len(self.buffer) - 4), self.buffer)
        return value
    
    def read_utf(self):
        length = 0
        self.read_short(length)
        string, self.buffer = struct.unpack('i%ds' % (len(self.buffer) - length), self.buffer)
        return string