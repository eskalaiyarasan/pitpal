import threading

from utils.events.event_base import BaseEventClass


class SingleEventClass(BaseEventClass):
    def __init__(self):
        self._subscribers = {}
        self._counter = 0
        self._lock = threading.Lock()

    def inc(self):
        with self._lock:
            if self._counter < 100000:
                self._counter += 1
                return hex(self._counter)
            return None

    def register(self, event_type, callback):
        self._subscribers.setdefault(event_type, []).append(callback)

    def notify(self, event_type, *args, **kwargs):
        event_num = self.inc()
        if event_type in self._subscribers:
            for callback in self._subscribers[event_type]:
                # Unpacking args and kwargs into the function
                callback(event_num, *args, **kwargs)
