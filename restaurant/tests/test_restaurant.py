from django.core.management import call_command
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITransactionTestCase

from portal.test_helpers import (get_portal_manager_token,
                                 get_restaurant_manager_token, )
from restaurant.models import Restaurant


class RestaurantAPITestCase(APITransactionTestCase):
    reset_sequences = True

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
        """Test the creation of a restaurant."""
        url = reverse('restaurants:restaurant-list')

        response = self.client.post(
            url, self.restaurant_data, format='json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_restaurant_without_auth(self):
        """Test the creation of a restaurant without auth."""
        url = reverse('restaurants:restaurant-list')

        response = self.client.post(
            url, self.restaurant_data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @get_portal_manager_token
    def test_restaurant_active_administrators_positive(self, token):
        """Test the that number for active administrators for Restaurant must
        be positive."""
        url = reverse('restaurants:restaurant-list')
        self.restaurant_data['active_administrators'] = -5
        response = self.client.post(
            url, self.restaurant_data, format='json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @get_portal_manager_token
    def test_restaurant_active_branches_positive(self, token):
        """Test the that number for active branches for Restaurant must
        be positive."""
        url = reverse('restaurants:restaurant-list')
        self.restaurant_data['active_branches'] = -5
        response = self.client.post(
            url, self.restaurant_data, format='json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @get_portal_manager_token
    def test_create_restaurant_manager(self, token):
        """Test the creation of a restaurant manager."""
        call_command('createrestaurants')
        url = reverse(
            'restaurants:restaurant-managers:restaurant-manager-list',
            kwargs={'restaurant_id': Restaurant.objects.all().first().id}
        )
        manager_data = {
            'username': 'TestRestaurantManager',
            'password': 'TestPassword'
        }
        response = self.client.post(
            url, manager_data, format='json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @get_restaurant_manager_token
    def test_create_branch(self, token):
        """Test the creation of a restaurant branch."""
        url = reverse(
            'restaurants:branch:branch-list',
            kwargs={'restaurant_id': Restaurant.objects.all().first().id}
        )
        branch_data = {
            'address': 'TestAddress',
            'phone_number': '555-555-5555',
        }
        response = self.client.post(
            url, branch_data, format='json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @get_portal_manager_token
    def test_delete_restaurant(self, token):
        """Test the deletion of a restaurant."""
        call_command('createrestaurants')

        url_get = reverse(
            'restaurants:restaurant-list',
        )
        response_get = self.client.get(
            url_get, format='json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'}
        )
        current_restaurants = len(response_get.data)

        url_delete = reverse(
            'restaurants:restaurant-detail',
            kwargs={
                'pk': Restaurant.objects.all().first().id,
            }
        )

        self.client.delete(
            url_delete, format='json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'}
        )

        response_get = self.client.get(
            url_get, format='json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'}
        )

        self.assertEqual(current_restaurants, len(response_get.data) + 1)
