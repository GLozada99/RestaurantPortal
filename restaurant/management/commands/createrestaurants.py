from django.core.management.base import BaseCommand
from django.db import transaction

from portal.command_helpers import CommandHelpers
from restaurant.models import Restaurant


class Command(BaseCommand):

    help = ('A command to populate the restaurant table.\n'
            'This command does not need parameters')

    @transaction.atomic
    def handle(self, *args, **kwargs):
        CommandHelpers.print_creating_message(self, 'Restaurant', 3)
        exists = Restaurant.objects.all().first()
        if exists:
            CommandHelpers.print_error(self, 'Delivery types already exist.')
        else:
            restaurant = [
                Restaurant(
                    name='McDonalds', food_type_id=1, active_branches=2,
                    active_administrators=2
                ),
                Restaurant(
                    name='Wendys', food_type_id=1, active_branches=2,
                    active_administrators=2
                ),
                Restaurant(
                    name='Burger King', food_type_id=1, active_branches=2,
                    active_administrators=2
                ),
            ]
            CommandHelpers.add_to_db(self, Restaurant, restaurant)
            CommandHelpers.print_success(self)
