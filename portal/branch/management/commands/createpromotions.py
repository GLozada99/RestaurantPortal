from django.core.management.base import BaseCommand
from django.db import transaction

from portal.branch.models import Combo, Promotion
from portal.command_helpers import CommandHelpers


class Command(BaseCommand):

    help = ('A command to populate the promotion table.\n'
            'This command does not need parameters')

    @transaction.atomic
    def handle(self, *args, **kwargs):
        CommandHelpers.print_creating_message(self, 'Promotion', 4)
        if Promotion.objects.all().exists():
            CommandHelpers.print_error(self, 'Promotion already exist.')
        else:
            promotion = [
                Promotion(name='Super Combo Ham', price=55, restaurant_id=1),
                Promotion(name='Super Combo Ham 2', price=56, restaurant_id=2),
                Promotion(name='Super Combo Ham 7', price=77, restaurant_id=1),
            ]
            CommandHelpers.add_to_db(self, Promotion, promotion)
            combo = [
                Combo(promotion=promotion[0], dish_id=1, quantity=2),
                Combo(promotion=promotion[2], dish_id=2, quantity=2),
                Combo(promotion=promotion[1], dish_id=1, quantity=1),
                Combo(promotion=promotion[1], dish_id=2, quantity=1),
            ]
            CommandHelpers.add_to_db(self, Combo, combo)

            CommandHelpers.print_success(self)
