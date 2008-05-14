from taskforce.base import BaseTask

__all__ = ('BaseTask', )

# task statuses
class TASK_STATUS(object):
    WAITING = 0
    ACTIVE = 1
    FINISHED = 2
    FAILED = 3