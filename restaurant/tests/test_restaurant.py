from django.core.management import call_command
from rest_framework.test import APITestCase


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
