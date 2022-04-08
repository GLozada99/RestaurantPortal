from django.core.management.base import BaseCommand
from django.db import transaction

from portal import settings
from portal.command_helpers import CommandHelpers
from portal.order.models import OrderStatus


class Command(BaseCommand):

    help = ('A command to populate the order status table.\n'
            'This command does not need parameters')

    @transaction.atomic
    def handle(self, *args, **kwargs):
        CommandHelpers.print_creating_message(self, 'OrderStatus', 7)
        if OrderStatus.objects.all().exists():
            CommandHelpers.print_error(self, 'OrderStatus already exists.')
        else:
            # Awaiting is for take-out or eat in, and delivering for delivery
            order_status = [
                OrderStatus(
                    name='Created',
                    position_order=settings.CREATED_POSITION_ORDER,
                ),
                OrderStatus(
                    name='Accepted',
                    position_order=settings.ACCEPTED_POSITION_ORDER,
                ),
                OrderStatus(
                    name='Rejected',
                    position_order=settings.REJECTED_POSITION_ORDER,
                ),
                OrderStatus(
                    name='Finished',
                    position_order=settings.FINISHED_POSITION_ORDER,
                ),
                OrderStatus(
                    name='Awaiting',
                    position_order=settings.AWAITING_POSITION_ORDER,
                ),
                OrderStatus(
                    name='Delivering',
                    position_order=settings.DELIVERING_POSITION_ORDER,
                ),
                OrderStatus(
                    name='Received',
                    position_order=settings.RECEIVED_POSITION_ORDER,
                ),
            ]
            CommandHelpers.add_to_db(self, OrderStatus, order_status)
            CommandHelpers.print_success(self)
