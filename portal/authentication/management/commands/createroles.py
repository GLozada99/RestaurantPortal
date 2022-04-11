from django.core.management.base import BaseCommand
from django.db import transaction

from portal.authentication.models import Role
from portal.command_helpers import CommandHelpers
from portal.settings import (
    BRANCH_MANAGER_LEVEL,
    CLIENT_LEVEL,
    EMPLOYEE_LEVEL,
    PORTAL_MANAGER_LEVEL,
    RESTAURANT_MANAGER_LEVEL,
)


class Command(BaseCommand):

    help = ('A command to populate the role table.\n'
            'This command does not need parameters')

    @transaction.atomic
    def handle(self, *args, **kwargs):
        CommandHelpers.print_creating_message(self, 'Role', 5)
        exists = Role.objects.filter(level=0)
        if exists:
            CommandHelpers.print_error(self, 'Roles already exist.')
        else:
            roles = [
                Role(
                    name='Portal Manager',
                    level=PORTAL_MANAGER_LEVEL,
                ),
                Role(
                    name='Restaurant Manager',
                    level=RESTAURANT_MANAGER_LEVEL,
                ),
                Role(name='Branch Manager', level=BRANCH_MANAGER_LEVEL),
                Role(name='Employee', level=EMPLOYEE_LEVEL),
                Role(name='Client', level=CLIENT_LEVEL),
            ]
            CommandHelpers.add_to_db(self, Role, roles)
            CommandHelpers.print_success(self)
