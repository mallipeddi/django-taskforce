import sys
from optparse import make_option

from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--verbose', action='store_true', dest='verbose',
            help = 'Verbose mode for you control freaks'),
    )
    help = """Stop taskforce server."""
    args = ""
    
    
    def _log(self, msg, error=False):
        if self._verbose or error:
            print msg
    
    def handle(self, *args, **options):
        # handle command-line options
        self._verbose = options.get('verbose', False)

        from taskforce.http import TaskforceDaemon
        self._log("Stop taskforce server...")
        TaskforceDaemon("/tmp/taskforce.pid").stop()
