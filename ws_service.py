from bottle import get, run, template
from bottle.ext.websocket import GeventWebSocketServer
from bottle.ext.websocket import websocket
import gevent
users = set()
@get('/', apply=[websocket])
def chat(ws):
    users.add(ws)
    while True:
        msg = ws.receive()
        if msg is not None:
            for u in users:
                print type(u)
                u.send(msg)
                print u,msg
        else: break
    users.remove(ws)
run(host='', port=10000, server=GeventWebSocketServer)