from django.core.management import call_command
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITransactionTestCase

from portal.test_helpers import (
    get_branch_manager_token,
    get_restaurant_manager_token,
)


class DishCategoryAPITestCase(APITransactionTestCase):

    reset_sequences = True

    category_data = {
        'name': 'TestDishCategory',
    }

    dish_category_list_url = reverse(
        'restaurants:dish-categories:dish-category-list',
        kwargs={'restaurant_id': 1},
    )

    def setUp(self) -> None:
        call_command('createroles')
        call_command('createdeliverytypes')
        call_command('createfoodtypes')
        call_command('createrestaurants')
        call_command('createbranches')

    @get_restaurant_manager_token
    def test_create_dish_category(self, token):
        """Test the creation of a dish category."""
        response = self.client.post(
            self.dish_category_list_url,
            self.category_data,
            format='json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @get_branch_manager_token
    def test_create_dish_category_wrong_token(self, token):
        """
        Test the creation of a dish category with branch manager token.
        """
        response = self.client.post(
            self.dish_category_list_url,
            self.category_data,
            format='json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @get_restaurant_manager_token
    def test_delete_dish_category(self, token):
        """Test the deletion of a dish category."""
        call_command('createdishcategories')
        response_get = self.client.get(
            self.dish_category_list_url,
            format='json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'},
        )
        current_categories = len(response_get.data)
        url_delete = reverse(
            'restaurants:dish-categories:dish-category-detail',
            kwargs={
                'restaurant_id': 1,
                'pk': response_get.data[0]['id'],
            },
        )
        self.client.delete(
            url_delete,
            format='json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'},
        )
        response_get = self.client.get(
            self.dish_category_list_url,
            format='json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'},
        )
        self.assertEqual(current_categories, len(response_get.data) + 1)
