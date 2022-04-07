from django.core.management import call_command
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from portal.test_helpers import get_portal_manager_token


class RoleAPITestCase(APITestCase):
    def setUp(self) -> None:
        call_command('createroles')

    @get_portal_manager_token
    def test_get_roles(self, token):
        """Test the get method of roles."""
        url = reverse('roles:role-list')
        response = self.client.get(
            url,
            format='json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_roles_without_auth(self):
        """Test the get method of roles without auth."""
        url = reverse('roles:role-list')
        response = self.client.get(
            url,
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
