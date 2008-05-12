import threading
import Queue

class ErrandSlave(threading.Thread):
    def __init__(self, todo, poll_timeout=5):
        threading.Thread.__init__(self)
        self.setDaemon(1)
        self._todo_queue = todo
        self._dismissed = threading.Event()
        self._poll_timeout = poll_timeout
        self.start()
    
    def run(self):
        while True:
            if self._dismissed.isSet():
                break
            try:
                errand = self._todo_queue.get(self._poll_timeout)
            except Queue.Empty:
                continue
            else:
                if self._dismissed.isSet():
                    self._todo_queue.put(errand)
                    break
                print "Working on a new errand..."

    def dismiss(self):
        self._dismissed.set()

class ErrandServiceState(object):
    def __init__(self):
        self._state = dict()
        self._lock = threading.RLock()
    
    def get_errand(self, id):
        if self._lock.acquire():
            try:
                return self._state[id]
            finally:
                self._lock.release()

    def add_errand(self, id, errand):
        if self._lock.acquire():
            try:
                self._state[id] = errand
            finally:
                self._lock.release()
    
    def del_errand(self, id):
        if self._lock.acquire():
            try:
                del self._state[id]
            finally:
                self._lock.release()

class ErrandService(object):
    def __init__(self, num_slaves=5):
        self._todo_queue = Queue.Queue()
        self._state = ErrandServiceState()
        self._slaves = []
        self._init_slaves(num_slaves)
    
    def _init_slaves(self, num_slaves):
        for i in range(num_slaves):
            self._slaves.append(
                ErrandSlave(todo = self._todo_queue)
            )

    def add_errand(self, errand):
        # add to todo queue
        self._todo_queue.put(errand, block=True, timeout=5) # TODO - handle queue full exception properly
        # maintain a record of new errand in service state
        self._state.add_errand(errand.id, errand)
        