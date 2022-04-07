from django.core.management.base import BaseCommand
from django.db import transaction

from dish.models import Dish, DishIngredient
from portal.command_helpers import CommandHelpers


class Command(BaseCommand):

    help = ('A command to populate the dish_category table.\n'
            'This command does not need parameters')

    @transaction.atomic
    def handle(self, *args, **kwargs):
        CommandHelpers.print_creating_message(self, 'Dish', 2)
        if Dish.objects.all().exists():
            CommandHelpers.print_error(self, 'Dish already exist.')
        else:
            dishes = [
                Dish(
                    name='Mozzarela Sticks', description='Goood',
                    price=10.99, category_id=1
                ),
                Dish(
                    name='Mojito', description='Goood',
                    price=15.79, category_id=2
                ),
                Dish(
                    name='Cheesecake', description='Goood',
                    price=15.79, category_id=3
                ),
            ]
            CommandHelpers.add_to_db(self, Dish, dishes)

            dish_ingredient = [
                DishIngredient(
                    dish_id=dishes[0].id, ingredient_id=1,
                    quantity=5, unit='Pounds'
                ),
                DishIngredient(
                    dish_id=dishes[0].id, ingredient_id=2,
                    quantity=3, unit='teaspoon'
                ),
                DishIngredient(
                    dish_id=dishes[1].id, ingredient_id=1,
                    quantity=2, unit='Kilograms'
                ),
                DishIngredient(
                    dish_id=dishes[1].id, ingredient_id=2,
                    quantity=1, unit='tablespoon'
                ),
                DishIngredient(
                    dish_id=dishes[2].id, ingredient_id=3,
                    quantity=1, unit='tablespoon'
                ),
            ]
            CommandHelpers.add_to_db(self, DishIngredient, dish_ingredient)
            CommandHelpers.print_success(self)
