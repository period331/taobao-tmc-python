# coding: utf8

from threading import Thread, Event
import time
import socket


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


class InitiativeQuery(Thread):
    def __init__(self, get_alive_client, log, frequency=30):

        Thread.__init__(self)
        self.frequency = frequency

        self.running = False
        self.reseting = False

        self.get_alive_client = get_alive_client
        self.log = log

        self.finished = Event()

    def __enter__(self):
        if self.frequency:
            self.start()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        _client = self.get_alive_client()
        if _client is not None:
            _client.on_error(_client, exc_type, exc_val, exc_tb)
        self.stop()

    def stop(self):
        self.running = False

    def reset_frequency(self):
        self.reseting = True

    def run(self):
        self.log('主动线程正在等待, %s s后启动' % self.frequency)
        self.finished.wait(self.frequency)

        self.running = True

        def _interval():
            for i in range(self.frequency):
                time.sleep(1)

                if not self.running:
                    break

                if self.reseting:
                    self.reseting = False
                    _interval()
                    break

            _client = self.get_alive_client()
            try:
                if _client is not None:
                    _client.send_query()
            except socket.error:
                _client.close()
            finally:
                _interval()

        _interval()

        self.finished.set()