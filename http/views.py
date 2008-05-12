from errands.base import *
from django.utils import simplejson

def errand_new(service):
    e = Errand()
    e.id = 'errand1'
    service.add_errand(e)
    return simplejson.dumps({'status':'success'})
