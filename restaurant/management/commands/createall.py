from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):

    help = ('A command to populate the delivery_type table.\n'
            'This command does not need parameters')

    @transaction.atomic
    def handle(self, *args, **kwargs):
        call_command('createroles')
        call_command('createfoodtypes')
        call_command('createdeliverytypes')
        call_command('createrestaurants')
        call_command('createdishcategories')
        call_command('createingredients')
        call_command('createdishes')
        call_command('createbranches')
        call_command('createinventories')
