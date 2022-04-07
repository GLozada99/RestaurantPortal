from django.core.management.base import BaseCommand
from django.db import transaction

from dish.models import Ingredient
from portal.command_helpers import CommandHelpers


class Command(BaseCommand):

    help = ('A command to populate the ingredient table.\n'
            'This command does not need parameters')

    @transaction.atomic
    def handle(self, *args, **kwargs):
        CommandHelpers.print_creating_message(self, 'Ingredient', 3)
        if Ingredient.objects.all().exists():
            CommandHelpers.print_error(
                self, 'Ingredients already exist.',
            )
        else:
            dish_categories = [
                Ingredient(name='Onion', restaurant_id=1),
                Ingredient(name='Ground Beef', restaurant_id=1),
                Ingredient(name='Lemon', restaurant_id=2),
            ]
            CommandHelpers.add_to_db(self, Ingredient, dish_categories)
            CommandHelpers.print_success(self)
