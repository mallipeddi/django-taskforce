import threading
import Queue

import taskforce
from taskforce.exceptions import TaskNotFound, TaskNotComplete

class Slave(threading.Thread):
    def __init__(self, todo, poll_timeout=5):  # TODO - think about the right poll_timeout
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
                task = self._todo_queue.get(self._poll_timeout)
                task.status = taskforce.TASK_STATUS.ACTIVE
                task._start()
                task.status = taskforce.TASK_STATUS.FINISHED
            except Queue.Empty:
                continue
            except Exception:
                task.status = taskforce.TASK_STATUS.FAILED

    def dismiss(self):
        self._dismissed.set()

class State(object):
    def __init__(self):
        self._state = dict()
        self._lock = threading.RLock()
    
    def get_task(self, id):
        if self._lock.acquire():
            try:
                return self._state[id]
            finally:
                self._lock.release()

    def add_task(self, id, task):
        if self._lock.acquire():
            try:
                self._state[id] = task
            finally:
                self._lock.release()
    
    def del_task(self, id):
        if self._lock.acquire():
            try:
                del self._state[id]
            finally:
                self._lock.release()

class TaskForce(object):
    def __init__(self, num_slaves=5):
        self._todo_queue = Queue.Queue()
        self._state = State()
        self._slaves = []
        self._init_slaves(num_slaves)
    
    def _init_slaves(self, num_slaves):
        for i in range(num_slaves):
            self._slaves.append(
                Slave(todo = self._todo_queue)
            )

    def add_task(self, task):
        # add to todo queue
        self._todo_queue.put(task, block=True, timeout=5) # TODO - handle queue full exception properly
        # maintain a record of new task in state
        self._state.add_task(task.id, task)
    
    def get_status(self, task_id):
        try:
            t = self._state.get_task(task_id)
        except KeyError:
            raise TaskNotFound("Task not found.")
        return t.status
    
    def get_progress(self, task_id):
        try:
            t = self._state.get_task(task_id)
        except KeyError:
            raise TaskNotFound("Task not found.")
        return t.progress
    
    def get_results(self, task_id):
        try:
            t = self._state.get_task(task_id)
        except KeyError:
            raise TaskNotFound("Task not found.")
        t_status = t.status
        print t_status
        if t_status != taskforce.TASK_STATUS.FINISHED and t_status != taskforce.TASK_STATUS.FAILED:
            raise TaskNotComplete("Cannot return results since tasks is not complete yet.")
