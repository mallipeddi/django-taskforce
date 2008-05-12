import sys

from django.core.management.base import BaseCommand
from django.conf import settings

from optparse import make_option
from errands.http import ErrandHTTPServer

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--verbose', action='store_true', dest='verbose',
            help = 'Verbose mode for you control freaks'),
    )
    help = """Run errand service."""
    #args = "[start|stop]"
    
    
    def _log(self, msg, error=False):
        if self._verbose or error:
            print msg
    
    def handle(self, *args, **options):
        # handle command-line options
        self._verbose = options.get('verbose', False)
        
        #if len(args) != 1:
        #    self._log("ERROR - Takes in exactly 1 arg (start|stop). %d were supplied." % len(args), error=True)
        #    sys.exit(1)
        #elif args[0] == "start":
        #    self._start()
        #elif args[0] == "stop":
        #    self._stop()
        #else:
        #    self._log("ERROR - Takes in exactly 1 arg (start|stop).", error=True)
        #    sys.exit(1)
        print "Starting HTTP server..."
        ErrandHTTPServer.start('127.0.0.1', 9000)
