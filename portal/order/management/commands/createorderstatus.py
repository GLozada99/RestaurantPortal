from django.core.management.base import BaseCommand
from django.db import transaction

from portal.order.models import OrderStatus
from portal.command_helpers import CommandHelpers


class Command(BaseCommand):

    help = ('A command to populate the order status table.\n'
            'This command does not need parameters')

    @transaction.atomic
    def handle(self, *args, **kwargs):
        CommandHelpers.print_creating_message(self, 'Branch', 4)
        if OrderStatus.objects.all().exists():
            CommandHelpers.print_error(self, 'OrderStatus already exists.')
        else:
            order_status = [
                OrderStatus(name='Cooking'),
                OrderStatus(name='Sending'),
                OrderStatus(name='Giving out'),
                OrderStatus(name='Done'),
            ]
            CommandHelpers.add_to_db(self, OrderStatus, order_status)
            CommandHelpers.print_success(self)
