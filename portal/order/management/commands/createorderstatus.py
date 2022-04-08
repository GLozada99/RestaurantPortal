from django.core.management.base import BaseCommand
from django.db import transaction

from portal.command_helpers import CommandHelpers
from portal.order.models import OrderStatus


class Command(BaseCommand):

    help = ('A command to populate the order status table.\n'
            'This command does not need parameters')

    @transaction.atomic
    def handle(self, *args, **kwargs):
        CommandHelpers.print_creating_message(self, 'Branch', 4)
        if OrderStatus.objects.all().exists():
            CommandHelpers.print_error(self, 'OrderStatus already exists.')
        else:
            # Awaiting is for take-out or eat in, and delivering for delivery
            order_status = [
                OrderStatus(name='Created'),
                OrderStatus(name='Accepted'),
                OrderStatus(name='Finished'),
                OrderStatus(name='Awaiting'),
                OrderStatus(name='Delivering'),
                OrderStatus(name='Received'),
            ]
            CommandHelpers.add_to_db(self, OrderStatus, order_status)
            CommandHelpers.print_success(self)
