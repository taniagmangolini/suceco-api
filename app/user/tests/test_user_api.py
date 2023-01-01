"""Tests for User API"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from rest_framework_simplejwt.tokens import AccessToken


CREATE_USER_URL = reverse('user:create')
CREATE_TOKEN_URL = reverse('token_obtain_pair')


def create_user(**params):
    """Create a new user."""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the public features from the API."""

    def setUp(self):
        self.client = APIClient()
        self.client_not_authenticated = APIClient()
        email = 'authenticated_user@test.com'
        password = 'strongP@assword!'
        authenticated_user = get_user_model().objects.create_user(
            email=email,
            password=password,
            name='Test Authenticated User'
        )
        token = AccessToken.for_user(user=authenticated_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_get_token_url_valid_credentials(self):
        """Test the url to get token_obtain_pair
        with valid credentials."""
        test_client = APIClient()
        user_data = {
            'email': 'unauthenticated_user@test.com',
            'password': 'strongP@assword!'
        }
        get_user_model().objects.create_user(
            email=user_data['email'],
            password=user_data['password'],
            name='Test unauthenticated User'
        )
        res = test_client.post(CREATE_TOKEN_URL,
                               user_data,
                               format='json')
        token = res.data['access']
        test_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_token_url_invalid_credentials(self):
        """Test the url to get token_obtain_pair
        with invalid credentials."""
        test_client = APIClient()
        user_data = {
            'email': 'invalid@test.com',
            'password': '12324354767'
        }
        res = test_client.post(CREATE_TOKEN_URL,
                               user_data,
                               format='json')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_user_when_not_authenticated(self):
        """Test a if an error will be returned if there is an
        attempt to create a user without previous authentication.
        """
        payload = {
            'email': 'new_user1@test.com',
            'password': 'password123',
            'name': 'New user 1'
        }
        res = self.client_not_authenticated.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_user_success(self):
        """Test a successful attempt to create a user;
        It validates the return code from the API (201),
        After that, it loads the user, check the password
        and also checks if password is not being returned in
        the api response (for security reasons, it should not
        be returned).
        """
        payload = {
            'email': 'new_user1@test.com',
            'password': 'password123',
            'name': 'New user 1'
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
            'email': 'new_user2@test.com',
            'password': 'password123',
            'name': 'New user 2'
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test a fail attempt to create a user with an
        password that is too short (less than 8 chars).
        """
        payload = {
            'email': 'new_user3@test.com',
            'password': '12345',
            'name': 'New user 3'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)
