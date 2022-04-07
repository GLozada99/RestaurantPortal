from django.core.management import call_command
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITransactionTestCase

from portal.test_helpers import (
    get_portal_manager_token,
    get_restaurant_manager_token,
)


class BranchAPITestCase(APITransactionTestCase):

    reset_sequences = True

    manager_data = {
        'username': 'TestManager',
        'password': 'TestPassword',
    }

    branch_list_url = reverse(
        'restaurants:branches:branch-list',
        kwargs={'restaurant_id': 1},
    )

    def setUp(self) -> None:
        call_command('createroles')
        call_command('createdeliverytypes')
        call_command('createfoodtypes')
        call_command('createrestaurants')
        call_command('createbranches')

    @get_restaurant_manager_token
    def test_create_branch(self, token):
        """Test the creation of a restaurant branch."""
        branch_data = {
            'address': 'TestAddress',
            'phone_number': '555-555-5555',
        }
        response = self.client.post(
            self.branch_list_url,
            branch_data,
            format='json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @get_restaurant_manager_token
    def create_more_branches_than_allowed(self, token):
        """Test creating more branches than allowed."""
        branch_data = {
            'address': 'TestAddress',
            'phone_number': '555-555-5555',
        }
        self.client.post(
            self.branch_list_url,
            branch_data,
            format='json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'},
        )
        response = self.client.post(
            self.branch_list_url,
            branch_data,
            format='json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @get_restaurant_manager_token
    def test_create_branch_manager(self, token):
        """Test the creation of a branch manager."""
        url = reverse(
            'restaurants:branches:branch-managers:branch-manager-list',
            kwargs={
                'restaurant_id': 1,
                'branch_id': 1,
            }
        )
        response = self.client.post(
            url,
            self.manager_data,
            format='json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @get_portal_manager_token
    def test_create_branch_manager_wrong_token(self, token):
        """Test the creation of a branch manager with portal manager user."""
        url = reverse(
            'restaurants:branches:branch-managers:branch-manager-list',
            kwargs={
                'restaurant_id': 1,
                'branch_id': 1,
            },
        )
        response = self.client.post(
            url,
            self.manager_data,
            format='json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @get_restaurant_manager_token
    def test_create_employee(self, token):
        """Test the creation of an employee."""
        call_command('createrestaurants')
        url = reverse(
            'restaurants:branches:employees:employee-list',
            kwargs={
                'restaurant_id': 1,
                'branch_id': 1,
            },
        )
        response = self.client.post(
            url,
            self.manager_data,
            format='json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @get_restaurant_manager_token
    def test_delete_branch(self, token):
        """Test the deletion of a branch."""
        response_get = self.client.get(
            self.branch_list_url,
            format='json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'},
        )
        current_branch = len(response_get.data)
        url_delete = reverse(
            'restaurants:branches:branch-detail',
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
            self.branch_list_url,
            format='json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'},
        )
        self.assertEqual(current_branch, len(response_get.data) + 1)
