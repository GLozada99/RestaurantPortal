from django.core.management import call_command
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITransactionTestCase

from portal.test_helpers import get_branch_manager_token


class InventoryAPITestCase(APITransactionTestCase):

    reset_sequences = True

    inventory_list_url = reverse(
        'restaurants:branches:inventory:inventory-list',
        kwargs={
            'restaurant_id': 1,
            'branch_id': 1,
        }
    )

    def setUp(self) -> None:
        call_command('createroles')
        call_command('createdeliverytypes')
        call_command('createfoodtypes')
        call_command('createrestaurants')
        call_command('createingredients')
        call_command('createbranches')

    @get_branch_manager_token
    def test_add_to_inventory(self, token):
        """Test adding ingredients to inventory."""
        ingredient_data = [
            {'ingredient': 1, 'stock': 5, 'unit': 'TestUnit'},
            {'ingredient': 2, 'stock': 5, 'unit': 'TestUnit'},
        ]
        for data in ingredient_data:
            response = self.client.post(
                self.inventory_list_url,
                data,
                format='json',
                **{'HTTP_AUTHORIZATION': f'Bearer {token}'},
            )
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @get_branch_manager_token
    def test_add_repeated_to_inventory(self, token):
        """Test adding repeated ingredient to inventory."""
        ingredient_data = [
            {'ingredient': 1, 'stock': 5, 'unit': 'TestUnit'},
            {'ingredient': 1, 'stock': 5, 'unit': 'TestUnit'},
        ]
        response = None
        for data in ingredient_data:
            response = self.client.post(
                self.inventory_list_url,
                data,
                format='json',
                **{'HTTP_AUTHORIZATION': f'Bearer {token}'},
            )
        # first response is 201, but second is 400
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @get_branch_manager_token
    def test_add_ingredient_other_restaurant(self, token):
        """Test adding ingredient from other restaurant to inventory."""
        ingredient_data = {
            'ingredient': 3,
            'stock': 5,
            'unit': 'TestUnit'
        }
        response = self.client.post(
            self.inventory_list_url,
            ingredient_data,
            format='json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @get_branch_manager_token
    def test_delete_inventory(self, token):
        """Test the deletion of an ingredient of inventory."""
        call_command('createinventories')
        response_get = self.client.get(
            self.inventory_list_url,
            format='json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'},
        )
        current_inventory_ingredients = len(response_get.data)
        url_delete = reverse(
            'restaurants:branches:inventory:inventory-detail',
            kwargs={
                'restaurant_id': 1,
                'branch_id': 1,
                'pk': response_get.data[0]['id'],
            }
        )
        self.client.delete(
            url_delete,
            format='json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'},
        )
        response_get = self.client.get(
            self.inventory_list_url,
            format='json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'},
        )
        self.assertEqual(
            current_inventory_ingredients, len(response_get.data) + 1
        )
