from django.core.management import call_command
from rest_framework.test import APITransactionTestCase


class IngredientAPITestCase(APITransactionTestCase):
    reset_sequences = True

    def setUp(self) -> None:
        call_command('createroles')
        call_command('createdeliverytypes')
        call_command('createfoodtypes')
