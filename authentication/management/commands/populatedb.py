from django.core.management.base import BaseCommand
from django.db import transaction
from psycopg2 import OperationalError

from authentication.models import Role


class Command(BaseCommand):

    help = ('A command to populate the database.\n'
            'This command does not need parameters')

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.create_roles()

    def print_creating_message(self, model, cuantity=10):
        self.stdout.write(
            f'Creating {cuantity} {model} records... ', ending=''
        )

    def print_success(self):
        self.stdout.write(self.style.SUCCESS('OK'))

    def print_error(self, msg):
        self.stdout.write(self.style.ERROR(f'ERROR. {msg}'))

    def add_to_db(self, model, records):
        try:
            model.objects.bulk_create(records)
        except OperationalError:
            self.print_error(
                'An error has occurred with the database connection.'
            )

    def create_roles(self):
        self.print_creating_message('Role', 5)
        exists = Role.objects.filter(level=0)
        if exists:
            self.print_error('Roles already exist')
        else:
            roles = [
                Role(name='Portal Manager', level=0),
                Role(name='Restaurant Manager', level=1),
                Role(name='Branch Manager', level=2),
                Role(name='Employee', level=3),
                Role(name='Client', level=4)
            ]
            self.add_to_db(Role, roles)
            self.print_success()
