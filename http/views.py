from django.utils import simplejson

import taskforce
from taskforce.base import *

def spit_errors(fn):
    def new_fn(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception, e:
            return simplejson.dumps({
                'error':str(e),
            })
    return new_fn

@spit_errors
def task_new(force, task_name, task_id):
    t = force.create_task(task_name)
    t.id = task_id
    force.add_task(t)
    return simplejson.dumps({
        'id':t.id,
    })

@spit_errors
def task_status(force, id):
    status = force.get_status(task_id = id)
    progress = force.get_progress(task_id = id)
    return simplejson.dumps({
        'status':status,
        'progress':progress,
    })

@spit_errors
def task_results(force, id):
    results = force.get_results(task_id = id)
    return simplejson.dumps(results)

