#!/usr/bin/env python
import sys
if sys.version_info[0] < 3:
    import Queue as q
else:
    import queue as q
import threading
import logging
import logging.handlers
from datetime import datetime, timedelta

def _send_loop(queue, sender, alive, timeout):
    while alive.is_set() or not queue.empty():
        try:
            msg = queue.get(alive.is_set(), timeout)
            sender.emit(msg)
            queue.task_done()
        except q.Empty:
            pass # check alive first


class _RawSocketHandler(logging.handlers.SocketHandler):
    def __init__(self, host, port):
        super(_RawSocketHandler, self).__init__(host, port)
        self.closeOnError = True

    def makePickle(self, record):
        return record.encode('utf-8') + b'\n'


class LogstashHandler(logging.Handler, object):
    def __init__(self, host, port,
                 level=logging.NOTSET, threads=1, queue_size=1000, timeout=1.0):
        super(LogstashHandler, self).__init__(level)
        self.queue = q.Queue(maxsize=queue_size)
        self.timeout = timeout
        self.alive = threading.Event()
        self.alive.set()
        self.workers = []
        for i in range(0, threads):
            socket = _RawSocketHandler(host, port)
            # TODO: check sock indeed created: socket.createSocket()
            sender = threading.Thread(target=_send_loop,
                                      args=(self.queue, socket,
                                            self.alive, self.timeout))
            sender.daemon=True
            sender.start()
            self.workers.append((socket, sender))

    def emit(self, record):
        if not self.alive.is_set():
            self.handleError(record)
        try:
            msg = self.format(record)
            self.queue.put_nowait(msg)
        except:
            self.handleError(record)

    def close(self):
        self.alive.clear()
        end = datetime.now() + timedelta(seconds=self.timeout)
        for socket, sender in self.workers:
            to = (end - datetime.now()).total_seconds()
            if to > 0.0:
                sender.join(timeout=to)
            if not sender.is_alive():
                socket.close()
        super(LogstashHandler, self).close()
