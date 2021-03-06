from datetime import date, timedelta
import copy

from django.core.management import call_command
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITransactionTestCase

from portal.test_helpers import get_restaurant_manager_token


class PromotionAPITestCase(APITransactionTestCase):

    reset_sequences = True

    promotion_data = {
        'name': 'Doble Melt',
        'price': 9.99,
        'branches': [1],
        'dishes': [
            {
                'dish': 1,
                'quantity': 2
            },
        ],
        'start_date': date.today(),
    }

    promotion_list_url = reverse(
        'restaurants:promotions:promotion-list', kwargs={'restaurant_id': 1}
    )

    def setUp(self) -> None:
        call_command('createroles')
        call_command('createdeliverytypes')
        call_command('createfoodtypes')
        call_command('createrestaurants')
        call_command('createdishcategories')
        call_command('createingredients')
        call_command('createdishes')
        call_command('createbranches')

    @get_restaurant_manager_token
    def test_create_promotion(self, token):
        """Test the creation of a promotion."""
        response = self.client.post(
            self.promotion_list_url,
            self.promotion_data,
            format='json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'},
        )
        self.assertEqual(response.data['branches'][0]['id'], 1)
        self.assertEqual(response.data['dishes'][0]['dish']['id'], 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @get_restaurant_manager_token
    def test_create_promotion_with_wrong_price(self, token):
        """Test the creation of a promotion with wrong price."""
        promotion_data = copy.deepcopy(self.promotion_data)
        promotion_data['price'] = 0
        response = self.client.post(
            self.promotion_list_url,
            promotion_data,
            format='json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['price'][0],
            'This field must be greater than zero.',
        )

    @get_restaurant_manager_token
    def test_create_promotion_with_wrong_start_date(self, token):
        """Test the creation of a promotion with wrong start date."""
        promotion_data = copy.deepcopy(self.promotion_data)
        promotion_data['start_date'] = date.today() - timedelta(days=10)
        response = self.client.post(
            self.promotion_list_url,
            promotion_data,
            format='json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['start_date'][0],
            'Invalid date, cannot be less than now.',
        )

    @get_restaurant_manager_token
    def test_create_promotion_with_wrong_finish_date(self, token):
        """Test the creation of a promotion with wrong finish date."""
        promotion_data = copy.deepcopy(self.promotion_data)
        promotion_data['finish_date'] = '2020-01-01'
        response = self.client.post(
            self.promotion_list_url,
            promotion_data,
            format='json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['finish_date'][0],
            'Invalid date, cannot be less than the start date.',
        )

    @get_restaurant_manager_token
    def test_create_promotion_with_wrong_quantity(self, token):
        """Test the creation of a promotion with wrong quantity."""
        promotion_data = copy.deepcopy(self.promotion_data)
        promotion_data['dishes'][0]['quantity'] = 0
        response = self.client.post(
            self.promotion_list_url,
            promotion_data,
            format='json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['dishes'][0]['quantity'][0],
            'This field must be greater than zero.',
        )

    @get_restaurant_manager_token
    def test_create_promotion_with_wrong_dish(self, token):
        """Test the creation of a promotion with a wrong dish."""
        promotion_data = copy.deepcopy(self.promotion_data)
        promotion_data['dishes'][0]['dish'] = 3
        response = self.client.post(
            self.promotion_list_url,
            promotion_data,
            format='json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['dishes'], 'Invalid dishes.')

    @get_restaurant_manager_token
    def test_create_promotion_with_wrong_branch(self, token):
        """Test the creation of a promotion with wrong branch."""
        promotion_data = copy.deepcopy(self.promotion_data)
        promotion_data['branches'] = [2]
        response = self.client.post(
            self.promotion_list_url,
            promotion_data,
            format='json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['branches'], 'Invalid branches.')
