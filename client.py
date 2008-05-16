"""taskforce client API.

Users use these methods to submit new tasks to the server,
fetch task status and results.
"""

import urllib, urllib2

from django.utils import simplejson

import taskforce
from taskforce import utils

class TaskforceError(Exception):
    pass

class TaskforceClient(object):

    @staticmethod
    def submit_new(task_id, cls, *args, **kwargs):
        """Submit new task to the server.
    
        task_id - id (string) for the task.
        cls - name of the Task class or the Task class itself.
        args, kwargs - args to the run() method of cls.
    
        Note - args, kwargs should be serializable via simplejson.
        """
        if isinstance(cls, type):
            cls = cls.__name__
        #print args, kwargs
        resp = urllib2.urlopen(utils.get_server_base_uri() + "/task/new/", urllib.urlencode({
                                                'task_id': task_id,
                                                'task_type': cls,
                                                'args':simplejson.dumps(args),
                                                'kwargs':simplejson.dumps(kwargs),
                                            })
                    )
        task = simplejson.loads(resp.read())
        if task.has_key('error'):
            raise TaskforceError(task['error'])

    @staticmethod
    def fetch_status(task_id):
        resp = urllib2.urlopen(utils.get_server_base_uri() + "/task/%s/" % task_id)
        task = simplejson.loads(resp.read())
        if not task.has_key('error'):
            return (task['status'], task['progress'])
        else:
            raise TaskforceError(task['error'])

    @staticmethod
    def has_finished(task_id):
        status, message = TaskforceClient.fetch_status(task_id)
        return status == taskforce.TASK_STATUS.FINISHED

    @staticmethod
    def fetch_results(task_id):
        resp = urllib2.urlopen(utils.get_server_base_uri() + "/task/%s/results/" % task_id, urllib.urlencode({}))
        task = simplejson.loads(resp.read())
        if not task.has_key('error'):
            return task['results']
        else:
            raise TaskforceError(task['error'])

