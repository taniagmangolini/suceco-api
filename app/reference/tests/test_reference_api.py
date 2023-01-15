"""Tests for Reference API"""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import Client

from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken

from core.models import Reference

from reference.serializers import ReferenceSerializer, \
    ReferenceDetailSerializer


CREATE_TOKEN_URL = reverse('token_obtain_pair')


REFERENCE_URL = reverse('reference:reference-list')


def detail_url(reference_id):
    """Create and return a a reference details.
    Used or update, patch and delete."""
    return reverse('reference:reference-detail', args=[reference_id])


def create_reference(**params):
    """Create and return reference."""
    reference = Reference.objects.create(publication=params['publication'],
                                         url=params['url'])
    return reference


class PublicReferenceAPITests(TestCase):
    """Test unauthenticated reference API."""

    def setUp(self):
        self.api_client = APIClient()
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@test.com',
            password='test123555',
        )
        self.client.force_login(self.admin_user)
        self.reference = create_reference(**{'publication': 'test',
                                             'url': 'www.teste.com'})

    def test_list_reference_no_auth_required(self):
        """Test list reference using the api
        when not authenticated."""
        res = self.api_client.get(REFERENCE_URL)
        reference = Reference.objects.filter(is_active=True).order_by('-id')
        serializer = ReferenceSerializer(reference, many=True)

        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEquals(res.data, serializer.data)

    def test_get_reference_detail_no_auth_required(self):
        """Test get reference detail with no authentication."""
        url = detail_url(self.reference.id)
        res = self.client.get(url)
        serializer = ReferenceDetailSerializer(self.reference)

        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEquals(res.data, serializer.data)


class PrivateReferenceAPITests(TestCase):
    """Test unauthenticated reference API."""

    def setUp(self):
        self.no_auth_client = APIClient()

        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@test.com',
            password='test123555',
        )
        self.client.force_login(self.admin_user)

        self.reference = create_reference(**{'publication': 'test',
                                             'url': 'www.teste.com'})
        self.api_client_admin = APIClient()
        admin_token = AccessToken.for_user(user=self.admin_user)
        autorization = f'Bearer {admin_token}'
        self.api_client_admin.credentials(HTTP_AUTHORIZATION=autorization)

    def test_delete_reference_not_authenticated(self):
        """Test delete a reference when not authenticated."""
        url = detail_url(self.reference.id)
        res = self.no_auth_client.delete(url)
        self.assertEquals(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_partial_update_reference_not_authenticated(self):
        """Test partial update of a reference when not authenticated."""
        payload = {'id': self.reference.id,
                   'publication': 'publication updated'}
        url = detail_url(self.reference.id)
        res = self.no_auth_client.patch(url, payload)
        self.assertEquals(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_full_update_reference_not_authenticated(self):
        """Test full update of a reference when not authenticated."""
        payload = {'id': self.reference.id,
                   'publication': 'publication full updated'}
        url = detail_url(self.reference.id)
        res = self.no_auth_client.put(url, payload)
        self.assertEquals(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_reference_not_authenticated(self):
        """Test create a reference when not authenticated."""
        payload = {'publication': 'new publication',
                   'url': 'www.teste.com'}
        res = self.no_auth_client.post(REFERENCE_URL, payload)
        self.assertEquals(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_referencedmin(self):
        """Test create a reference when user is admin."""
        payload = {'publication': 'new publication',
                   'url': 'www.teste.com'}
        res = self.api_client_admin.post(REFERENCE_URL,
                                         payload,
                                         format='json')
        self.assertEquals(res.status_code, status.HTTP_201_CREATED)

    def test_partial_update_referencedmin(self):
        """Test partial update of a reference when user is admin."""
        new_publication = 'publication partial update'
        payload = {'id': self.reference.id,
                   'publication': new_publication}
        url = detail_url(self.reference.id)
        res = self.api_client_admin.patch(url, payload)
        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.reference.refresh_from_db()
        self.assertEquals(self.reference.publication, new_publication)

    def test_delete_referencedmin(self):
        """Test delete a reference when user is admin."""
        url = detail_url(self.reference.id)
        res = self.api_client_admin.delete(url)
        self.assertEquals(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Reference.objects.filter(id=self.reference.id)
                         .exists())
