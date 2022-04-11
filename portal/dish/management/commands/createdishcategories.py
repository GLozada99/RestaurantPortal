from django.core.management.base import BaseCommand
from django.db import transaction

from portal.command_helpers import CommandHelpers
from portal.dish.models import DishCategory


class Command(BaseCommand):

    help = ('A command to populate the dish_category table.\n'
            'This command does not need parameters')

    @transaction.atomic
    def handle(self, *args, **kwargs):
        CommandHelpers.print_creating_message(self, 'DishCategory', 3)
        if DishCategory.objects.all().exists():
            CommandHelpers.print_error(
                self, 'Dish categories already exist.',
            )
        else:
            dish_categories = [
                DishCategory(name='Entree', restaurant_id=1),
                DishCategory(name='Drinks', restaurant_id=1),
                DishCategory(name='Dessert', restaurant_id=2),
            ]
            CommandHelpers.add_to_db(self, DishCategory, dish_categories)
            CommandHelpers.print_success(self)
