# coding: utf8

from threading import Thread, Event
import time


class TaobaoWsThread(Thread):
    def __init__(self, client, interval=1):
        Thread.__init__(self)

        self.client = client
        self.interval = interval  # 延迟启动时间
        self.finished = Event()

    def run(self):
        self.finished.wait(self.interval)

        if not self.finished.is_set():
            self.client.run_forever()

        self.finished.set()


class HeartbeatThread(Thread):
    """ 心跳包线程 """

    def __init__(self, connections, interval=50, log=lambda message: None):
        Thread.__init__(self)
        self.connections = list(connections)
        self.interval = interval
        self.log = log

        self.running = True

    def run(self):
        while self.running:
            for i in range(self.interval):
                time.sleep(1)
            for ws in self.connections:
                ws.ping()

    def stop(self):
        self.running = False