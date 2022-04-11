from django.core.management.base import BaseCommand
from django.db import transaction

from portal.branch.models import Branch
from portal.command_helpers import CommandHelpers


class Command(BaseCommand):

    help = ('A command to populate the branch table.\n'
            'This command does not need parameters')

    @transaction.atomic
    def handle(self, *args, **kwargs):
        CommandHelpers.print_creating_message(self, 'Branch', 4)
        if Branch.objects.all().exists():
            CommandHelpers.print_error(self, 'Branches already exist.')
        else:
            branches = [
                Branch(
                    restaurant_id=1, address='Here',
                    phone_number='555-555-5555',
                ),
                Branch(
                    restaurant_id=2, address='There',
                    phone_number='555-555-6666',
                ),
                Branch(
                    restaurant_id=3, address='Away',
                    phone_number='555-555-7777',
                ),
                Branch(
                    restaurant_id=1, address='Close',
                    phone_number='555-555-8888',
                ),
            ]
            CommandHelpers.add_to_db(self, Branch, branches)
            CommandHelpers.print_success(self)
