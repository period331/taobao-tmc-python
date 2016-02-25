# coding: utf-8
__author__ = 'baocaixiong'

import logging

from tornado import ioloop
from tornado.options import parse_command_line

from tmcclient import TmcClient


if __name__ == '__main__':
    cli = parse_command_line()

    logging.basicConfig(level=logging.DEBUG)
    ws = TmcClient('ws://mc.api.taobao.com/', '1021737885', 'sandboxbbf5579605d7936422c11af0e', 'default',
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

