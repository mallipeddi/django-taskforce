"""taskforce client API.

Users use these method calls to submit new tasks to the server,
fetch task status and results.
"""

import urllib, urllib2

from django.utils import simplejson

import taskforce
from taskforce.utils import jsonify

BASE_URL = "http://localhost:9000"

@jsonify
def submit_new(task_id, cls, *args, **kwargs):
    """Submit new task to the server.
    
    task_id - id (string) for the task.
    cls - name of the Task class or the Task class itself.
    args, kwargs - args to the run() method of cls.
    
    Note - args, kwargs should be serializable via simplejson.
    """
    if isinstance(cls, type):
        cls = cls.__name__
    resp = urllib2.urlopen(BASE_URL + "/task/new/", urllib.urlencode({
                                                'task_id': task_id,
                                                'task_type': cls,
                                                'args':simplejson.dumps(args),
                                                'kwargs':simplejson.dumps(kwargs),
                                            })
                    )
    return resp.read()

@jsonify
def fetch_status(task_id):
    resp = urllib2.urlopen(BASE_URL + "/task/%s/" % task_id)
    return resp.read()

@jsonify
def fetch_results(task_id):
    resp = urllib2.urlopen(BASE_URL + "/task/%s/results/" % task_id, urllib.urlencode({}))
    return resp.read()
