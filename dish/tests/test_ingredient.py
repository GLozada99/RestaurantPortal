from django.core.management import call_command
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITransactionTestCase

from dish.models import Ingredient
from portal.test_helpers import (get_branch_manager_token,
                                 get_restaurant_manager_token, )
from restaurant.models import Restaurant


class IngredientAPITestCase(APITransactionTestCase):
    reset_sequences = True

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

    @get_branch_manager_token
    def test_create_ingredient_wrong_token(self, token):
        """Test the creation of an ingredient with branch
        manager token."""
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
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @get_restaurant_manager_token
    def test_delete_dish_category(self, token):
        """Test the deletion of a dish category."""
        call_command('createingredients')
        url_get = reverse(
            'restaurants:ingredients:ingredient-list',
            kwargs={'restaurant_id': Restaurant.objects.all().first().id}
        )
        response_get = self.client.get(
            url_get, format='json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'}
        )
        current_ingredients = len(response_get.data)

        url_delete = reverse(
            'restaurants:ingredients:ingredient-detail',
            kwargs={
                'restaurant_id': Restaurant.objects.all().first().id,
                'pk': Ingredient.objects.all().first().id
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

        self.assertEqual(current_ingredients, len(response_get.data) + 1)
