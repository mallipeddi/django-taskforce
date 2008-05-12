from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
from errands.service import ErrandService

from django.core.urlresolvers import get_resolver

_resolver = get_resolver('errands.http.urls')
service = None

class ErrandHTTPServer(ThreadingMixIn, HTTPServer):
    @staticmethod
    def start(address, port):
        global service
        service = ErrandService()
        ErrandHTTPServer((address, port), ErrandHTTPRequestHandler).serve_forever()

class ErrandHTTPRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        print "Creating instance of ErrandHTTPRequestHandler..."
        BaseHTTPRequestHandler.__init__(self, *args, **kwargs)

    def do_GET(self):
        view_func, view_args, view_kwargs = _resolver.resolve(self.path)
        try:
            resp = view_func(service = service, *view_args, **view_kwargs)
            self.send_response(200, 'OK')
            self.end_headers()
            self.wfile.write(resp)
        except Exception, e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(e)

