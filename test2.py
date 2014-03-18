# coding: utf-8

from websocketpy import WebSocketConnection, WebSocketServer
from utils import createSign
import time
import socket

app_key = '1021737885'
group_name = 'default'
secret = 'sandboxbbf5579605d7936422c11af0e'
timestamp = int(time.time())


sock = socket.socket()

service = WebSocketServer()

conn = WebSocketConnection(sock, 'ws://mc.api.tbsandbox.com/')


conn.send("0app_key1021737885group_namedefaulttimestamp%ssign%ssdk2" % (timestamp, createSign(app_key, group_name, secret, timestamp)))


result =  conn.recv()

