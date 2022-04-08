from django.core.management import call_command
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITransactionTestCase

from portal.test_helpers import get_client_token


class OrderAPITestCase(APITransactionTestCase):

    reset_sequences = True

    order_list_url = reverse(
        'restaurants:branches:order:order-list',
        kwargs={
            'restaurant_id': 1,
            'branch_id': 1,
        },
    )

    def setUp(self) -> None:
        call_command('createall')

    @get_client_token
    def test_create_order(self, token):
        """Test the creation of a restaurant branch."""
        order_data = {
            'delivery_type': 1,
            'address': 'Here',
            'dishes': [{
                'dish': 1,
                'quantity': 1,
            }],
        }
        response = self.client.post(
            self.order_list_url,
            order_data,
            format='json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
