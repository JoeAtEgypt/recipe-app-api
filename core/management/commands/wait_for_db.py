# time: the default Python Module that we can use to make our apps sleep for a few seconds.
import time

# connections: Module which is what we can use to test if the database is available.
from django.db import connections
from django.db.utils import OperationalError

# baseCommand: class that we need to build on to create our Custom Command.
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    """ Django command to pause execution util database is available """

    # we put our code in a handle function: ran whenever we run this management command.
    # ("*args", "**options"): allow for passing in custom arguments and options to our management commands.
    def handle(self, *args, **options):
        self.stdout.write('waiting for database...')
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database Available!'))

