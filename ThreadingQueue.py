import threading

class ThreadingQueue:

    def __init__(self):
        self.queue = []
        self.empty = threading.Semaphore(24)
        self.full = threading.Semaphore(0)
        self.lock = threading.Lock()

    def enqueue(self,item):
        self.empty.acquire()
        self.lock.acquire()
        self.queue.append(item)
        self.lock.release()
        self.full.release()


    def dequeue(self):
        self.full.acquire()
        self.lock.acquire()
        val = self.queue.pop(0)
        self.lock.release()
        self.empty.release()
        return val
