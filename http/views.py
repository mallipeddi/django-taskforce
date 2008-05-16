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
def task_new(force, task_type, task_id, run_args, run_kwargs):
    run_args = simplejson.loads(run_args)
    run_kwargs = simplejson.loads(run_kwargs)
    t = force.create_task(task_type, task_id, run_args, run_kwargs)
    force.add_task(t)
    return simplejson.dumps({
        'task_id':task_id,
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
    return simplejson.dumps({
        'results':results
    })

