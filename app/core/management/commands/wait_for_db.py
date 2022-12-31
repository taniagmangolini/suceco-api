"""
Django command to wait for database to be available.
"""
import time
import os
from django.core.management.base import BaseCommand
from django.db.utils import OperationalError

from psycopg2 import OperationalError as Psycopg2Error


class Command(BaseCommand):
    """Django command to wait for database."""

    def handle(self, *args, **options):
        """Entrypoint for command."""
        self.stdout.write('Connecting to database host {}'.format(os.environ.get('DB_HOST')))
        self.stdout.write('Connecting to database name {}'.format(os.environ.get('DB_NAME')))
        self.stdout.write('waiting for db...')
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2Error, OperationalError):
                self.stdout.write('database unavailable, waiting 1 second ...')
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('Database available!'))
