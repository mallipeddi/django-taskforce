from taskforce.base import BaseTask
from taskforce.client import TaskforceClient as Taskforce
from taskforce.client import TaskforceError

# task statuses
class TASK_STATUS(object):
    WAITING = 0
    ACTIVE = 1
    FINISHED = 2
    FAILED = 3

__all__ = ('BaseTask', 'Taskforce', 'TaskforceError', 'TASK_STATUS', )
