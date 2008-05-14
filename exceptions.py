class TaskNotComplete(Exception):
    "The requested task is not complete."
    pass

class TaskNotFound(Exception):
    "The requested tasks was not found."
    pass

class TaskTypeNotFound(Exception):
    "The requested type of task is not recognized."
    pass

class TaskFailed(Exception):
    "The requested task failed."
    pass
