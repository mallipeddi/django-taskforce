class TaskNotComplete(Exception):
    "The requested task is not complete."
    pass

class TaskNotFound(Exception):
    "The requested tasks was not found."
    pass
