from django.core.management import call_command
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITransactionTestCase

from branch.models import Branch
from portal.test_helpers import get_restaurant_manager_token
from restaurant.models import Restaurant


class BranchAPITestCase(APITransactionTestCase):
    reset_sequences = True

    def setUp(self) -> None:
        call_command('createroles')
        call_command('createdeliverytypes')
        call_command('createfoodtypes')
        call_command('createrestaurants')
        call_command('createbranches')
        self.restaurant_id = Restaurant.objects.all().first().id
        self.branch_id = Branch.objects.filter(
            restaurant_id=self.restaurant_id
        ).first().id

    @get_restaurant_manager_token
    def test_create_branch(self, token):
        """Test the creation of a restaurant branch."""
        url = reverse(
            'restaurants:branches:branch-list',
            kwargs={'restaurant_id': self.restaurant_id}
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

    @get_restaurant_manager_token
    def test_create_branch_manager(self, token):
        """Test the creation of a branch manager."""
        call_command('createrestaurants')
        url = reverse(
            'restaurants:branches:branch-managers:branch-manager-list',
            kwargs={
                'restaurant_id': self.restaurant_id,
                'branch_id': self.branch_id
            }
        )
        manager_data = {
            'username': 'TestBranchManager',
            'password': 'TestPassword'
        }
        response = self.client.post(
            url, manager_data, format='json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @get_restaurant_manager_token
    def test_create_employee(self, token):
        """Test the creation of an employee."""
        call_command('createrestaurants')
        url = reverse(
            'restaurants:branches:employees:employee-list',
            kwargs={
                'restaurant_id': self.restaurant_id,
                'branch_id': self.branch_id
            }
        )
        manager_data = {
            'username': 'TestEmployee',
            'password': 'TestPassword'
        }
        response = self.client.post(
            url, manager_data, format='json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
