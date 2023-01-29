"""Tests for species API"""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import Client

from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken

from core.models import Species

from species.serializers import SpeciesSerializer, SpeciesDetailSerializer


CREATE_TOKEN_URL = reverse('token_obtain_pair')


SPECIES_URL = reverse('species:species-list')


def detail_url(species_id):
    """Create and return a a species details.
    Used or update, patch and delete."""
    return reverse('species:species-detail', args=[species_id])


def create_species(**params):
    """Create and return species."""
    species = Species.objects.create(scientific_name=params['scientific_name'])
    return species


class PublicSpeciesAPITests(TestCase):
    """Test unauthenticated species API.
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
        self.species_a = create_species(**{'scientific_name': 'Sp test 1'})
        self.species_b = create_species(**{'scientific_name': 'Sp test 2'})

    def test_list_species_no_auth_required(self):
        """Test list species using the api
        when not authenticated."""
        res = self.api_client.get(SPECIES_URL)
        species = Species.objects.filter(is_active=True).order_by('-id')
        serializer = SpeciesSerializer(species, many=True)

        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEquals(res.data.get('results'), serializer.data)

    def test_get_species_detail_no_auth_required(self):
        """Test get species detail with no authentication."""
        url = detail_url(self.species_a.id)
        res = self.client.get(url)
        serializer = SpeciesDetailSerializer(self.species_a)

        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEquals(res.data, serializer.data)


class PrivateSpeciesAPITests(TestCase):
    """Test unauthenticated species API."""

    def setUp(self):
        self.no_auth_client = APIClient()

        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@test.com',
            password='test123555',
        )
        self.client.force_login(self.admin_user)

        self.species_a = create_species(**{'scientific_name': 'Species Test'})

        self.api_client_admin = APIClient()
        admin_token = AccessToken.for_user(user=self.admin_user)
        autorization = f'Bearer {admin_token}'
        self.api_client_admin.credentials(HTTP_AUTHORIZATION=autorization)

    def test_delete_species_not_authenticated(self):
        """Test delete a species when not authenticated."""
        url = detail_url(self.species_a.id)
        res = self.no_auth_client.delete(url)
        self.assertEquals(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_partial_update_species_not_authenticated(self):
        """Test partial update of a species when not authenticated."""
        payload = {'id': self.species_a.id,
                   'scientific_name': 'new scientific_name'}
        url = detail_url(self.species_a.id)
        res = self.no_auth_client.patch(url, payload)
        self.assertEquals(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_full_update_species_not_authenticated(self):
        """Test full update of a species when not authenticated."""
        payload = {'id': self.species_a.id,
                   'scientific_name': 'new scientific_name'}
        url = detail_url(self.species_a.id)
        res = self.no_auth_client.put(url, payload)
        self.assertEquals(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_species_not_authenticated(self):
        """Test create a species when not authenticated."""
        payload = {'scientific_name': 'new species'}
        res = self.no_auth_client.post(SPECIES_URL, payload)
        self.assertEquals(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_species_admin(self):
        """Test create a species when user is admin."""
        payload = {'scientific_name': 'New species Test Admin'}
        res = self.api_client_admin.post(SPECIES_URL, payload, format='json')
        self.assertEquals(res.status_code, status.HTTP_201_CREATED)

    def test_partial_update_species_admin(self):
        """Test partial update of a species when user is admin."""
        payload = {'id': self.species_a.id,
                   'scientific_name': 'partial updated scientific_name'}
        url = detail_url(self.species_a.id)
        res = self.api_client_admin.patch(url, payload)
        self.assertEquals(res.status_code, status.HTTP_200_OK)

    def test_delete_species_admin(self):
        """Test delete a species when user is admin."""
        url = detail_url(self.species_a.id)
        res = self.api_client_admin.delete(url)
        self.assertEquals(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Species.objects.filter(id=self.species_a.id).exists())
