# coding: utf-8

from threading import Thread
import time
import sys


class _Thread(Thread):
    def __init__(self, *args, **kwargs):
        super(_Thread, self).__init__(*args, **kwargs)

        self.name = 'zhangming'
        self.running = False

    def run(self):
        self.running = True
        print 123123
        time.sleep(0.1)
        self.running = False


try:
    raise Exception('hehe')
except Exception, e:
    print type(sys.exc_info()[1]) == sys.exc_info()[0]


# if __name__ == "__main__":
#     t = _Thread()

#     t.daemon = True
#     t.start()

#     for i in range(0, 100):
#         print t.running
#         time.sleep(0.1)

