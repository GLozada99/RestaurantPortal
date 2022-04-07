from django.core.management import call_command
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITransactionTestCase

from dish.models import DishCategory, Ingredient
from portal.test_helpers import get_restaurant_manager_token


class DishAPITestCase(APITransactionTestCase):

    reset_sequences = True

    dish_data = {
        'name': 'TestDish',
        'price': 49.99,
        'description': 'Test Description...',
        'ingredients': None,
    }

    dish_list_url = reverse(
        'restaurants:dish-category:dish:dish-list',
        kwargs={'restaurant_id': 1, 'dish_category_id': 1},
    )

    def setUp(self) -> None:
        call_command('createroles')
        call_command('createdeliverytypes')
        call_command('createfoodtypes')
        call_command('createrestaurants')
        call_command('createdishcategories')
        call_command('createingredients')

    @get_restaurant_manager_token
    def test_create_dish(self, token):
        """Test the creation of a dish."""
        ingredients = [
            {
                'ingredient': ing.id,
                'quantity': 5,
                'unit': 'TestUnit',
            } for ing in Ingredient.objects.filter(
                restaurant_id=1
            )
        ]
        self.dish_data['ingredients'] = ingredients
        response = self.client.post(
            self.dish_list_url,
            self.dish_data,
            format='json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'},
        )
        dish = DishCategory.objects.get(id=1).dish_set.filter(
            name='TestDish',
        ).first()
        for ingredient, dish_ingredient in zip(
            dish.ingredients.all(), ingredients,
        ):
            self.assertEqual(ingredient.id, dish_ingredient['ingredient'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @get_restaurant_manager_token
    def test_create_dish_repeated_ingredients(self, token):
        """Test the creation of a dish with repeated ingredients."""
        ingredients = [
            {
                'ingredient': 1,
                'quantity': 5,
                'unit': 'TestUnit',
            } for _ in range(2)
        ]
        self.dish_data['ingredients'] = ingredients
        response = self.client.post(
            self.dish_list_url,
            self.dish_data,
            format='json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @get_restaurant_manager_token
    def test_delete_restaurant(self, token):
        """Test the deletion of a dish."""
        call_command('createdishes')
        response_get = self.client.get(
            self.dish_list_url, format='json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'},
        )
        current_dishes = len(response_get.data)
        url_delete = reverse(
            'restaurants:dish-category:dish:dish-detail',
            kwargs={
                'restaurant_id': 1,
                'dish_category_id': 1,
                'pk': response_get.data[0]['id'],
            },
        )
        self.client.delete(
            url_delete,
            format='json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'},
        )
        response_get = self.client.get(
            self.dish_list_url,
            format='json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'},
        )
        self.assertEqual(current_dishes, len(response_get.data) + 1)
