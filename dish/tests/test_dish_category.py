from django.core.management import call_command
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from portal.test_helpers import (get_branch_manager_token,
                                 get_restaurant_manager_token, )
from restaurant.models import Restaurant


class DishCategoryAPITestCase(APITestCase):

    def setUp(self) -> None:
        call_command('createroles')
        call_command('createdeliverytypes')
        call_command('createfoodtypes')

    @get_restaurant_manager_token
    def test_create_dish_category(self, token):
        """Test the creation of a dish category."""
        url = reverse(
            'restaurants:dish-categories:dish-category-list',
            kwargs={'restaurant_id': Restaurant.objects.all().first().id}
        )
        category_data = {
            'name': 'TestDishCategory',
        }
        response = self.client.post(
            url, category_data, format='json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @get_branch_manager_token
    def test_create_dish_category_wrong_token(self, token):
        """Test the creation of a dish category with branch manager token."""
        url = reverse(
            'restaurants:dish-categories:dish-category-list',
            kwargs={'restaurant_id': Restaurant.objects.all().first().id}
        )
        category_data = {
            'name': 'TestDishCategory',
        }
        response = self.client.post(
            url, category_data, format='json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
