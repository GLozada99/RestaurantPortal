from django.core.management import call_command
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from portal.test_helpers import get_portal_manager_token


class PortalManagerAPITestCase(APITestCase):
    def setUp(self) -> None:
        call_command('createroles')

    @get_portal_manager_token
    def test_create_portal_manager(self, token):
        """Test the creation of a portal manager."""
        url = reverse('portal_managers:portal-manager-list')
        response = self.client.post(
            url,
            {'username': 'TestPortalManager', 'password': 'TestPassword'},
            format='json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_portal_manager_without_auth(self):
        """Test the creation of a portal manager without auth."""
        url = reverse('portal_managers:portal-manager-list')
        response = self.client.post(
            url,
            {'username': 'TestPortalManager', 'password': 'TestPassword'},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ClientAPITestCase(APITestCase):
    def setUp(self) -> None:
        call_command('createroles')

    def test_create_client(self):
        """Test the creation of a client."""
        url = reverse('clients:client-list')
        response = self.client.post(
            url,
            {'username': 'TestClient', 'password': 'TestPassword'},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
