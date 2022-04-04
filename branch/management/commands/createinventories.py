from django.core.management.base import BaseCommand
from django.db import transaction

from branch.models import Inventory
from portal.command_helpers import CommandHelpers


class Command(BaseCommand):

    help = ('A command to populate the inventory table.\n'
            'This command does not need parameters')

    @transaction.atomic
    def handle(self, *args, **kwargs):
        CommandHelpers.print_creating_message(self, 'Inventory', 4)
        exists = Inventory.objects.all().first()
        if exists:
            CommandHelpers.print_error(self, 'Inventory already exist.')
        else:
            inventory = [
                Inventory(
                    branch_id=1, ingredient_id=1,
                    stock=5, unit='Pounds'
                ),
                Inventory(
                    branch_id=1, ingredient_id=2,
                    stock=3, unit='teaspoon'
                ),
                Inventory(
                    branch_id=2, ingredient_id=1,
                    stock=2, unit='Kilograms'
                ),
                Inventory(
                    branch_id=2, ingredient_id=2,
                    stock=1, unit='tablespoon'
                ),
            ]
            CommandHelpers.add_to_db(self, Inventory, inventory)
            CommandHelpers.print_success(self)
