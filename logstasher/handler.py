#!/usr/bin/env python3.4
import logging
import logging.handlers
import queue as q
import threading


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
        super().__init__(host, port)
        self.closeOnError = True

    def makePickle(self, record):
        return record.encode('utf-8') + b'\n'


class LogstashHandler(logging.Handler, object):
    def __init__(self, host, port,
                 level=logging.NOTSET, threads=1, queue_size=1000):
        super().__init__(level)
        self.queue = q.Queue(maxsize=queue_size)
        self.alive = threading.Event()
        self.alive.set()
        self.workers = []
        for i in range(0, threads):
            socket = _RawSocketHandler(host, port)
            # TODO: check sock indeed created: socket.createSocket()
            sender = threading.Thread(target=_send_loop, daemon=True,
                                      args=(self.queue, socket, self.alive),
                                      kwargs=dict(timeout=1.0/threads))
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
        for socket, sender in self.workers:
            if hasattr(socket.sock, 'gettimeout'):
                sender.join(timeout=socket.sock.gettimeout())
            if not sender.is_alive():
                socket.close()
        super().close()
