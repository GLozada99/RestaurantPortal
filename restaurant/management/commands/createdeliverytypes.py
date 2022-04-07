from django.core.management.base import BaseCommand
from django.db import transaction

from portal.command_helpers import CommandHelpers
from restaurant.models import DeliveryType


class Command(BaseCommand):

    help = ('A command to populate the delivery_type table.\n'
            'This command does not need parameters')

    @transaction.atomic
    def handle(self, *args, **kwargs):
        CommandHelpers.print_creating_message(self, 'DeliveryType', 3)
        if DeliveryType.objects.filter(name='Delivery').exists():
            CommandHelpers.print_error(self, 'Delivery types already exist.')
        else:
            delivery_types = [
                DeliveryType(name='Delivery'),
                DeliveryType(name='Take Out'),
                DeliveryType(name='Eat Here'),
            ]
            CommandHelpers.add_to_db(self, DeliveryType, delivery_types)
            CommandHelpers.print_success(self)
