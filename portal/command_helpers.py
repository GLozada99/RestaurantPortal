from django.core.management.base import BaseCommand
from psycopg2 import OperationalError


class CommandHelpers():

    def print_creating_message(command: BaseCommand, model, cuantity=10):
        command.stdout.write(
            f'Creating {cuantity} {model} records... ', ending=''
        )

    def print_success(command: BaseCommand):
        command.stdout.write(command.style.SUCCESS('OK'))

    def print_error(command: BaseCommand, msg):
        command.stdout.write(command.style.ERROR(f'ERROR. {msg}'))

    def add_to_db(command: BaseCommand, model, records):
        try:
            model.objects.bulk_create(records)
        except OperationalError:
            command.print_error(
                'An error has occurred with the database connection.'
            )
