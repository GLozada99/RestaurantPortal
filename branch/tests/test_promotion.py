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
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @get_restaurant_manager_token
    def test_create_promotion_with_wrong_price(self, token):
        """Test the creation of a promotion with wrong price."""
        self.promotion_data['price'] = 0
        response = self.client.post(
            self.promotion_list_url,
            self.promotion_data,
            format='json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'},
        )
        self.promotion_data['price'] = 9.99
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['price'][0],
            'This field must be greater than zero.',
        )

    @get_restaurant_manager_token
    def test_create_promotion_with_wrong_quantity(self, token):
        """Test the creation of a promotion with wrong quantity."""
        self.promotion_data['dishes'][0]['quantity'] = 0
        response = self.client.post(
            self.promotion_list_url,
            self.promotion_data,
            format='json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'},
        )
        self.promotion_data['dishes'][0]['quantity'] = 2
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['dishes'][0]['quantity'][0],
            'This field must be greater than zero.',
        )

    @get_restaurant_manager_token
    def test_create_promotion_with_wrong_dish(self, token):
        """Test the creation of a promotion with a wrong dish."""
        self.promotion_data['dishes'][0]['dish'] = 3
        response = self.client.post(
            self.promotion_list_url,
            self.promotion_data,
            format='json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'},
        )
        self.promotion_data['dishes'][0]['dish'] = 1
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['dishes'], 'Invalid dishes.')

    @get_restaurant_manager_token
    def test_create_promotion_with_wrong_branch(self, token):
        """Test the creation of a promotion with wrong branch."""
        self.promotion_data['branches'] = [2]
        response = self.client.post(
            self.promotion_list_url,
            self.promotion_data,
            format='json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'},
        )
        self.promotion_data['branches'] = [1]
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['branches'], 'Invalid branches.')
