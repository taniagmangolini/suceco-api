"""Tests for Register API"""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import Client

from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken # noqa

from core.models import Register

from register.serializers import RegisterSerializer, \
    RegisterDetailSerializer

from model_bakery import baker

from utils.constants import StateType, StageType


CREATE_TOKEN_URL = reverse('token_obtain_pair')


REFERENCE_URL = reverse('register:register-list')


def detail_url(register_id):
    """Create and return a a register details.
    Used or update, patch and delete."""
    return reverse('register:register-detail', args=[register_id])


def create_register(**params):
    """Create and return register."""

    register = Register.objects.create(reference=params['reference'],
                                       species=params['species'],
                                       forest=params['forest'],
                                       stage=params['stage'],
                                       state=params['state'])
    return register


class PublicRegisterAPITests(TestCase):
    """Test unauthenticated Register API."""

    def setUp(self):
        self.api_client = APIClient()
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@test.com',
            password='test123555',
        )
        self.client.force_login(self.admin_user)
        self.reference = baker.make('Reference')
        self.forest = baker.make('Forest')
        self.species = baker.make('Species')
        self.register = create_register(**{'reference': self.reference,
                                           'forest': self.forest,
                                           'species': self.species,
                                           'stage': StageType.PIONEIRA,
                                           'state': StateType.SP})

    def test_list_register_no_auth_required(self):
        """Test list Register using the api
        when not authenticated."""
        res = self.api_client.get(REFERENCE_URL)
        register = Register.objects.filter(is_active=True).order_by('-id')
        serializer = RegisterSerializer(register, many=True)

        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEquals(res.data, serializer.data)

    def test_get_register_detail_no_auth_required(self):
        """Test get register detail with no authentication."""
        url = detail_url(self.register.id)
        res = self.client.get(url)
        serializer = RegisterDetailSerializer(self.register)

        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEquals(res.data, serializer.data)


class PrivateRegisterAPITests(TestCase):
    """Test authenticated Register API."""

    def setUp(self):
        self.no_auth_client = APIClient()
        self.reference = baker.make('Reference')
        self.forest = baker.make('Forest')
        self.species = baker.make('Species')
        self.register = create_register(**{'reference': self.reference,
                                           'forest': self.forest,
                                           'species': self.species,
                                           'stage': StageType.PIONEIRA,
                                           'state': StateType.SP})

    def test_delete_register_not_authenticated(self):
        """Test delete a register when not authenticated."""
        url = detail_url(self.register.id)
        res = self.no_auth_client.delete(url)
        self.assertEquals(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_partial_update_register_not_authenticated(self):
        """Test partial update of a register when not authenticated."""
        payload = {'id': self.register.id,
                   'stage': StageType.SECUNDARIA}
        url = detail_url(self.register.id)
        res = self.no_auth_client.patch(url, payload)
        self.assertEquals(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_full_update_register_not_authenticated(self):
        """Test full update of a register when not authenticated."""
        payload = {'id': self.register.id,
                   'stage': StageType.SECUNDARIA_INICIAL}
        url = detail_url(self.register.id)
        res = self.no_auth_client.put(url, payload)
        self.assertEquals(res.status_code, status.HTTP_401_UNAUTHORIZED)
