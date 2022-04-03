from django.core.management import call_command
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from portal.test_helpers import (get_restaurant_manager_token, )
from restaurant.models import Restaurant


class IngredientAPITestCase(APITestCase):

    def setUp(self) -> None:
        call_command('createroles')
        call_command('createdeliverytypes')
        call_command('createfoodtypes')

    @get_restaurant_manager_token
    def test_create_ingredient(self, token):
        """Test the creation of an ingredient."""
        url = reverse(
            'restaurants:ingredients:ingredient-list',
            kwargs={'restaurant_id': Restaurant.objects.all().first().id}
        )
        ingredient_data = {
            'name': 'TestIngredient',
        }
        response = self.client.post(
            url, ingredient_data, format='json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
