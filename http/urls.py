from django.conf.urls.defaults import *

urlpatterns = patterns('taskforce.http.views',
    (r'^task/new/$', 'task_new'),
    (r'^task/(?P<id>\w+)/$', 'task_status'),
    (r'^task/(?P<id>\w+)/results/$', 'task_results'),
)