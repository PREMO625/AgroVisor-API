import threading
from queue import Queue

class RequestQueue:
    def __init__(self, maxsize=10):
        self.queue = Queue(maxsize=maxsize)
        self.lock = threading.Lock()

    def add_request(self, request):
        with self.lock:
            self.queue.put(request)

    def get_request(self):
        with self.lock:
            return self.queue.get()
