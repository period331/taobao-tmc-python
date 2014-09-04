taobao-tmc-python
=======================

淘宝平台消息服务python版本

usage:
```python
logging.basicConfig(level=logging.DEBUG)
    ws = TmcClient('ws://mc.api.tbsandbox.com/', '1021737885', 'sandboxbbf5579605d7936422c11af0e', 'default',
        query_message_interval=50)
    def print1():
        print 'on_open'
    ws.on("on_open", print1)
    try:
        ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        pass
    finally:
        ws.close()
```
