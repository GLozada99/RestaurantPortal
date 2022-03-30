from django.core.management.base import BaseCommand
from django.db import transaction

from portal.command_helpers import CommandHelpers
from restaurant.models import FoodType


class Command(BaseCommand):

    help = ('A command to populate the food_type table.\n'
            'This command does not need parameters')

    @transaction.atomic
    def handle(self, *args, **kwargs):
        CommandHelpers.print_creating_message(self, 'FoodType', 3)
        exists = FoodType.objects.filter(name='American')
        if exists:
            CommandHelpers.print_error(self, 'Food types already exist.')
        else:
            food_types = [
                FoodType(name='American'),
                FoodType(name='Mexican'),
                FoodType(name='Chinese'),
                FoodType(name='Italian'),
            ]
            CommandHelpers.add_to_db(self, FoodType, food_types)
            CommandHelpers.print_success(self)
