import threading

from django.conf import settings
import taskforce

class BaseTask(object):
    """Base class for all tasks.
    
    Users are expected to implement their own Task classes by sub-classing this class.
    """
    def __init__(self):
        self._lock = threading.RLock()
        self._status = taskforce.TASK_STATUS.WAITING
        self._progress = None
        self._results = None
    
    def _get_status(self):
        if self._lock.acquire():
            try:
                return self._status
            finally:
                self._lock.release()
    def _set_status(self, status):
        if self._lock.acquire():
            try:
                self._status = status
            finally:
                self._lock.release()
    status = property(_get_status, _set_status)
    
    def _get_progress(self):
        if self._lock.acquire():
            try:
                return self._progress
            finally:
                self._lock.release()
    def _set_progress(self, progress):
        if self._lock.acquire():
            try:
                self._progress = progress
            finally:
                self._lock.release()
    progress = property(_get_progress, _set_progress)
    
    def _get_results(self):
        if self._lock.acquire():
            try:
                return self._results
            finally:
                self._lock.release()
    def _set_results(self, results):
        if self._lock.acquire():
            try:
                self._results = results
            finally:
                self._lock.release()
    results = property(_get_results, _set_results)
    
    def _start(self, run_args=(), run_kwargs={}):
        def _new_start():
            self._results = self.run(*run_args, **run_kwargs)
        self._start = _new_start
    
    def run(self):
        "Implement this method in your sub-classes. This is where the meat of a Task goes."
        pass
