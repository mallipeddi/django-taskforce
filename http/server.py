"""
Implements HTTP API on top of web.py
"""

import web

from django.core.urlresolvers import get_resolver

from taskforce.daemon import Daemon
from taskforce.service import TaskForce
from taskforce.http.views import *

force = None

# routes
urls = (
    r'^/task/new/$', 'handle_task_new',
    r'^/task/(?P<id>\w+)/$', 'handle_task_status',
    r'^/task/(?P<id>\w+)/results/$', 'handle_task_results',
)

# views
class handle_task_new:
    def POST(self):
        i = web.input()
        print task_new(force, 
                task_type = i.task_type,
                task_id = i.task_id,
                run_args = i.args,
                run_kwargs = i.kwargs
            )

class handle_task_status:
    def GET(self, id):
        print task_status(force, id)

class handle_task_results:
    def POST(self, id):
        print task_results(force, id)


def runserver(available_tasks, pool_size, address):
    global force
    force = TaskForce(available_tasks = available_tasks, pool_size = pool_size)
    web.runsimple(web.webapi.wsgifunc(web.webpyfunc(urls, globals())), address)

class TaskforceDaemon(Daemon):
    def run(self, *args, **kwargs):
        runserver(*args, **kwargs)
