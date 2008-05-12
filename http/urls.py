from django.conf.urls.defaults import *

urlpatterns = patterns('errands.http.views',
    (r'^errand/new/$', 'errand_new'),
    (r'^errand/(?P<id>\w+)/$', 'errand_status'),
    (r'^errand/(?P<id>\w+)/results/$', 'errand_results'),
)