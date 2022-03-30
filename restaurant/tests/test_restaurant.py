from django.core.management import call_command
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from portal.test_helpers import get_portal_manager_token


class RestaurantAPITestCase(APITestCase):

    def setUp(self) -> None:
        call_command('createroles')
        call_command('createdeliverytypes')
        call_command('createfoodtypes')
        self.restaurant_data = {
            'name': 'TestRestaurant',
            'food_type': 1,
            'active_branches': 5,
            'active_administrators': 5,
            'delivery_types': [1, 2]
        }

    @get_portal_manager_token
    def test_create_restaurant(self, token):
        """Test the creation of a category."""
        url = reverse('restaurants:restaurant-list')

        response = self.client.post(
            url, self.restaurant_data, format='json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_restaurant_without_auth(self):
        """Test the creation of a category without auth."""
        url = reverse('restaurants:restaurant-list')

        response = self.client.post(
            url, self.restaurant_data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
