import web

from django.core.urlresolvers import get_resolver

from taskforce.service import TaskForce
from taskforce.http.views import *

force = None

urls = (
    r'^/task/new/$', 'handle_task_new',
    r'^/task/(?P<id>\w+)/$', 'handle_task_status',
    r'^/task/(?P<id>\w+)/results/$', 'handle_task_results',
)

class handle_task_new:
    def POST(self):
        i = web.input()
        print task_new(force, task_name = i.task_name, task_id = i.task_id)

class handle_task_status:
    def GET(self, id):
        print task_status(force, id)

class handle_task_results:
    def POST(self, id):
        print task_results(force, id)

def runserver(available_tasks, address):
    global force
    force = TaskForce(available_tasks = available_tasks)
    web.runsimple(web.webapi.wsgifunc(web.webpyfunc(urls, globals())), address)