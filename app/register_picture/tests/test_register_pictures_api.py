"""Tests for Register Picture API"""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import Client

from rest_framework import status
from rest_framework.test import APIClient

from core.models import RegisterPicture

from register.serializers import RegisterPictureSerializer

from model_bakery import baker


CREATE_TOKEN_URL = reverse('token_obtain_pair')


REGISTER_PICTURE_URL = reverse('register_picture:registerpicture-list')


def detail_url(id):
    """Create and return a a register picture.
    Used or update, patch and delete."""
    return reverse('register_picture:registerpicture-detail', args=[id])


class PublicRegisterPictureAPITests(TestCase):
    """Test unauthenticated Register Picture API."""

    def setUp(self):
        self.api_client = APIClient()
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@test.com',
            password='test123555',
        )
        self.picture = baker.make('RegisterPicture')

    def test_list_register_pictures_no_auth_required(self):
        """Test list Register using the api
        when not authenticated."""
        res = self.api_client.get(REGISTER_PICTURE_URL)
        register = RegisterPicture.objects.filter(is_active=True)\
            .order_by('-id')
        serializer = RegisterPictureSerializer(register, many=True)

        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEquals(res.data, serializer.data)

    def test_get_register_detail_no_auth_required(self):
        """Test get register detail with no authentication."""
        url = detail_url(self.picture.id)
        res = self.client.get(url)
        serializer = RegisterPictureSerializer(self.picture)

        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEquals(res.data, serializer.data)
