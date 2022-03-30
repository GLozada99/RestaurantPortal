from django.core.management import call_command
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from portal.test_helpers import get_portal_manager_token


class UserAPITestCase(APITestCase):
    def setUp(self) -> None:
        call_command('populatedb')

    @get_portal_manager_token
    def test_create_portal_manager(self, token):
        """Test the creation of a category."""
        url = reverse('portal_managers:portal-manager-list')
        response = self.client.post(
            url,
            {'username': 'TestPortalManager', 'password': 'TestPassword'},
            format='json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
