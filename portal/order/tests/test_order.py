from django.core.management import call_command
from django.db.models import Model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITransactionTestCase

from portal.branch.models import Promotion
from portal.dish.models import Dish
from portal.test_helpers import get_client_token, get_employee_token


def calculate_cost(model: Model, data: list, key: str):
    return sum((
        float(model.objects.get(pk=row[key]).price * row['quantity'])
        for row in data
    ))


class OrderAPITestCase(APITransactionTestCase):

    reset_sequences = True

    order_list_url = reverse(
        'restaurants:branches:order:order-list',
        kwargs={
            'restaurant_id': 1,
            'branch_id': 1,
        },
    )

    order_data = {
        'delivery_type': 1,
        'address': 'Here',
        'dishes': [
            {
                'dish': 1,
                'quantity': 1,
            },
            {
                'dish': 2,
                'quantity': 2,
            }
        ],
    }

    def setUp(self) -> None:
        call_command('createall')

    @get_client_token
    def test_create_order(self, token):
        """Test the creation of an order."""

        response = self.client.post(
            self.order_list_url,
            self.order_data,
            format='json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @get_employee_token
    def test_create_order_wrong_token(self, token):
        """Test the creation of an order with wrong token."""
        response = self.client.post(
            self.order_list_url,
            self.order_data,
            format='json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @get_client_token
    def test_total_cost_correct(self, token):
        """Test the correct calculation of total_cost field on order."""
        total_cost = calculate_cost(
            Dish, self.order_data.get('dishes', []), 'dish'
        ) + calculate_cost(
            Promotion, self.order_data.get('promotions', []), 'promotion'
        )
        response = self.client.post(
            self.order_list_url,
            self.order_data,
            format='json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'},
        )
        self.assertEqual(total_cost, response.data['total_cost'])

    @get_client_token
    def test_dishes_promotions_none(self, token):
        """Test the error when creating order if not dishes ."""
        self.order_data['dishes'] = None
        self.order_data['promotions'] = None

        response = self.client.post(
            self.order_list_url,
            self.order_data,
            format='json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @get_client_token
    def test_dishes_another_restaurant(self, token):
        """
        Test the error when creating order with dishes from another
        restaurant.
        """
        self.order_list_url = reverse(
            'restaurants:branches:order:order-list',
            kwargs={
                'restaurant_id': 3,
                'branch_id': 3,
            },
        )

        response = self.client.post(
            self.order_list_url,
            self.order_data,
            format='json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
