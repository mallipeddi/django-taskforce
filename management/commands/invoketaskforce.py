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
    args = "[thread-pool size]"
    
    
    def _log(self, msg, error=False):
        if self._verbose or error:
            print msg
    
    def handle(self, *args, **options):
        # handle command-line options
        self._verbose = options.get('verbose', False)
        
        if len(args) == 0:
            pool_size = 5
        elif len(args) == 1:
            pool_size = int(args[0])
        else:
            self._log("ERROR - Takes in exactly 1 optional arg. %d were supplied." % len(args), error=True)
            sys.exit(1)
        
        address, port = taskforce.utils.get_server_loc()
        
        available_tasks = []
        for app_name in settings.INSTALLED_APPS:
            app_mod = __import__(app_name, {}, {}, ['tasks'])
            if hasattr(app_mod, 'tasks'):
                for k in app_mod.tasks.__dict__.values():
                    if isinstance(k, type) and issubclass(k, taskforce.BaseTask):
                        available_tasks.append(k)
        
        print "Starting HTTP server..."
        runserver(available_tasks, pool_size, (address, port))
