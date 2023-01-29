"""Tests for Forest API"""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import Client

from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken

from core.models import Forest

from forest.serializers import ForestSerializer, ForestDetailSerializer

from utils.constants import DomainType


CREATE_TOKEN_URL = reverse('token_obtain_pair')


FOREST_URL = reverse('forest:forest-list')


def detail_url(forest_id):
    """Create and return a forest details.
    Used or update, patch and delete."""
    return reverse('forest:forest-detail', args=[forest_id])


def create_forest(**params):
    """Create and return forest."""
    forest = Forest.objects.create(name=params['name'],
                                   domain=DomainType.MATA_ATLANTICA)
    return forest


class PublicForestAPITests(TestCase):
    """Test unauthenticated forest API.
    See:
    https://www.django-rest-framework.org/api-guide/
    routers/#routing-for-extra-actions"""

    def setUp(self):
        self.api_client = APIClient()
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@test.com',
            password='test123555',
        )
        self.client.force_login(self.admin_user)
        self.forest_a = create_forest(**{'name': 'Forest Test X'})
        self.forest_b = create_forest(**{'name': 'Forest Test Y'})

    def test_list_forest_no_auth_required(self):
        """Test list forests using the api
        when not authenticated."""
        res = self.api_client.get(FOREST_URL)
        forests = Forest.objects.filter(is_active=True).order_by('-id')
        serializer = ForestSerializer(forests, many=True)

        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEquals(res.data.get('results'), serializer.data)

    def test_get_forest_detail_no_auth_required(self):
        """Test get forest detail with no authentication."""
        url = detail_url(self.forest_a.id)
        res = self.client.get(url)
        serializer = ForestDetailSerializer(self.forest_a)

        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEquals(res.data, serializer.data)


class PrivateForestAPITests(TestCase):
    """Test unauthenticated forest API."""

    def setUp(self):
        self.no_auth_client = APIClient()

        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@test.com',
            password='test123555',
        )
        self.client.force_login(self.admin_user)

        self.forest_a = create_forest(**{'name': 'Forest Test A'})

        self.api_client_admin = APIClient()
        admin_token = AccessToken.for_user(user=self.admin_user)
        autorization = f'Bearer {admin_token}'
        self.api_client_admin.credentials(HTTP_AUTHORIZATION=autorization)

    def test_delete_forest_not_authenticated(self):
        """Test delete a forest when not authenticated."""
        url = detail_url(self.forest_a.id)
        res = self.no_auth_client.delete(url)
        self.assertEquals(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_partial_update_forest_not_authenticated(self):
        """Test partial update of a forest when not authenticated."""
        payload = {'id': self.forest_a.id,
                   'domain': DomainType.CERRADO.name}
        url = detail_url(self.forest_a.id)
        res = self.no_auth_client.patch(url, payload)
        self.assertEquals(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_full_update_forest_not_authenticated(self):
        """Test full update of a forest when not authenticated."""
        payload = {'id': self.forest_a.id,
                   'name': 'Forest changed',
                   'domain': DomainType.CERRADO.name}
        url = detail_url(self.forest_a.id)
        res = self.no_auth_client.put(url, payload)
        self.assertEquals(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_forest_not_authenticated(self):
        """Test create a forest when not authenticated."""
        payload = {'name': 'New Forest Test',
                   'domain': DomainType.AMAZONIA.name}
        res = self.no_auth_client.post(FOREST_URL, payload)
        self.assertEquals(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_forest_admin(self):
        """Test create a forest when user is admin."""
        payload = {'name': 'New Forest Test',
                   'domain': DomainType.AMAZONIA.name}
        res = self.api_client_admin.post(FOREST_URL, payload, format='json')
        self.assertEquals(res.status_code, status.HTTP_201_CREATED)

    def test_partial_update_forest_admin(self):
        """Test partial update of a forest when user is admin."""
        payload = {'id': self.forest_a.id,
                   'domain': DomainType.CERRADO.name}
        url = detail_url(self.forest_a.id)
        res = self.api_client_admin.patch(url, payload)
        self.assertEquals(res.status_code, status.HTTP_200_OK)

    def test_delete_forest_admin(self):
        """Test delete a forest when user is admin."""
        url = detail_url(self.forest_a.id)
        res = self.api_client_admin.delete(url)
        self.assertEquals(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Forest.objects.filter(id=self.forest_a.id).exists())
