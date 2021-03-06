from django.core.management.base import BaseCommand
from django.db import transaction

from portal.command_helpers import CommandHelpers
from portal.restaurant.models import Restaurant


class Command(BaseCommand):

    help = ('A command to populate the restaurant table.\n'
            'This command does not need parameters')

    @transaction.atomic
    def handle(self, *args, **kwargs):
        CommandHelpers.print_creating_message(self, 'Restaurant', 3)
        if Restaurant.objects.all().exists():
            CommandHelpers.print_error(self, 'Restaurant already exist.')
        else:
            restaurants = [
                Restaurant(
                    name='McDonalds', food_type_id=1, active_branches=3,
                    active_administrators=2,
                ),
                Restaurant(
                    name='Wendys', food_type_id=1, active_branches=3,
                    active_administrators=2,
                ),
                Restaurant(
                    name='Burger King', food_type_id=1, active_branches=3,
                    active_administrators=2,
                ),
            ]
            CommandHelpers.add_to_db(self, Restaurant, restaurants)

            for restaurant in restaurants:
                restaurant.delivery_types.set([1, 2, 3])
                restaurant.save()

            CommandHelpers.print_success(self)
