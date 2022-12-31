"""Tests for User API"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    """Create a new user."""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the public features from the API."""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test a successful attempt to create a user;
        It validates the return code from the API (201),
        After that, it loads the user, check the password
        and also checks if password is not being returned in
        the api response (for security reasons, it should not
        be returned).
        """
        payload = {
            'email': 'new_user@test.com',
            'password': 'password123',
            'name': 'Persons name'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_create_user_with_a_existent_email(self):
        """Test a fail attempt to create a user with an
        email that already exists.
        """
        payload = {
            'email': 'new_user@test.com',
            'password': 'password123',
            'name': 'Persons name'
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test a fail attempt to create a user with an
        password that is too short (less than 8 chars).
        """
        payload = {
            'email': 'new_user@test.com',
            'password': '1234567',
            'name': 'Persons name'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)
