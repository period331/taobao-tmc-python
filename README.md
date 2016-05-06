### taobao-tmc-python

淘宝平台消息服务python版本

usage:
```
import taobaotmcpy
import tornado
import logging

logging.basicConfig(level=logging.DEBUG)

ws = taobaotmcpy.TmcClient('ws://mc.api.tbsandbox.com/', 'appkey', 'appsecret', 'default',
    query_message_interval=50)
def print1():
    print 'on_open'

ws.on("on_open", print1)

try:
    tornado.ioloop.IOLoop.instance().start()
except KeyboardInterrupt:
    pass
finally:
    ws.close()

```
或者
```
python2 -m taobaotmcpy
```
