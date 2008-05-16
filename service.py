import threading
import Queue

import taskforce
from taskforce.exceptions import TaskNotFound, TaskNotComplete, TaskTypeNotFound

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
            except Exception, e:
                # TODO - figure out a way to display this exception in error msg
                task.status = taskforce.TASK_STATUS.FAILED
                print e

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
    def __init__(self, available_tasks=[], num_slaves=5):
        self._todo_queue = Queue.Queue()
        self._state = State()
        self._slaves = []
        self._init_slaves(num_slaves)
        self._init_tasks(available_tasks)
    
    def _init_tasks(self, available_tasks):
        if not hasattr(self, '_available_tasks'):
            self._available_tasks = dict()
        for t in available_tasks:
            self._available_tasks[t.__name__] = t
    
    def _init_slaves(self, num_slaves):
        for i in range(num_slaves):
            self._slaves.append(
                Slave(todo = self._todo_queue)
            )

    def create_task(self, task_type, task_id, run_args, run_kwargs):
        if self._available_tasks.has_key(task_type):
            t = self._available_tasks[task_type].__call__()
            t.id = task_id
            t._start(run_args, run_kwargs)
            return t
        else:
            raise TaskTypeNotFound("Task of type %s not recognised." % task_type)

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
        if t_status == taskforce.TASK_STATUS.FINISHED:
            self._state.del_task(task_id)
            return t.results
        elif t_status == taskforce.TASK_STATUS.FAILED:
            raise TaskFailed("Cannot return results because task failed.")
        else:
            raise TaskNotComplete("Cannot return results because task is not complete yet.")
