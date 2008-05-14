from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
from taskforce.service import TaskForce

from django.core.urlresolvers import get_resolver

_resolver = get_resolver('taskforce.http.urls')
force = None

class TaskForceHTTPServer(ThreadingMixIn, HTTPServer):
    @staticmethod
    def start(address, port):
        global force
        force = TaskForce()
        TaskForceHTTPServer((address, port), TaskForceHTTPRequestHandler).serve_forever()

class TaskForceHTTPRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        BaseHTTPRequestHandler.__init__(self, *args, **kwargs)

    def do_GET(self):
        view_func, view_args, view_kwargs = _resolver.resolve(self.path)
        try:
            resp = view_func(force, *view_args, **view_kwargs)
            self.send_response(200, 'OK')
            self.end_headers()
            self.wfile.write(resp)
        except Exception, e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(e)

