import sys
from optparse import make_option

from django.core.management.base import BaseCommand
from django.conf import settings

import taskforce
from taskforce.http import runserver

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--verbose', action='store_true', dest='verbose',
            help = 'Verbose mode for you control freaks'),
    )
    help = """Run taskforce server."""
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
        
        available_tasks = []
        for app_name in settings.INSTALLED_APPS:
            app_mod = __import__(app_name, {}, {}, ['tasks'])
            if hasattr(app_mod, 'tasks'):
                for k in app_mod.tasks.__dict__.values():
                    if isinstance(k, type) and issubclass(k, taskforce.BaseTask):
                        available_tasks.append(k)
        
        print "Starting HTTP server..."
        runserver(available_tasks, ('127.0.0.1', 9000))
