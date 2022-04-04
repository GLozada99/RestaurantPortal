from django.core.management import call_command
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITransactionTestCase

from branch.models import Branch
from portal.test_helpers import (get_branch_manager_token,
                                 )
from restaurant.models import Restaurant


class InventoryAPITestCase(APITransactionTestCase):
    reset_sequences = True

    def setUp(self) -> None:
        call_command('createroles')
        call_command('createdeliverytypes')
        call_command('createfoodtypes')
        call_command('createrestaurants')
        call_command('createingredients')
        call_command('createbranches')
        self.restaurant_id = Restaurant.objects.all().first().id
        self.branch_id = Branch.objects.filter(
            restaurant_id=self.restaurant_id
        ).first().id

    @get_branch_manager_token
    def test_add_to_inventory(self, token):
        """Test adding ingredients to inventory."""
        url = reverse(
            'restaurants:branches:inventory:inventory-list',
            kwargs={
                'restaurant_id': self.restaurant_id,
                'branch_id': self.branch_id,
            }
        )
        ingredient_data = [
            {'ingredient': 1,
             'stock': 5,
             'unit': 'TestUnit'},
            {'ingredient': 2,
             'stock': 5,
             'unit': 'TestUnit'},
        ]
        for data in ingredient_data:
            response = self.client.post(
                url, data, format='json',
                **{'HTTP_AUTHORIZATION': f'Bearer {token}'}
            )
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
