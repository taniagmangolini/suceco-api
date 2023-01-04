"""
Test for models.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models
from utils.constants import DomainsType


class ModelTest(TestCase):
    """Test model"""

    def test_create_user_with_email_successful(self):
        """Test creating user with an email.
        and check if the authentication is ok by manually
        authenticate a user by comparing a plain-text password to
        the hashed password in the database."""
        email = 'test@test.com'
        password = 'abc1233456'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test if email is normalized."""
        emails = [
            ['test@TEST.com', 'test@test.com'],
            ['Test2@test.com', 'Test2@test.com'],
            ['TEST3@TEST.com', 'TEST3@test.com'],
            ['test4@test.COM', 'test4@test.com'],
        ]

        for email, expected_email in emails:
            user = get_user_model().objects.create_user(
                email=email,
                password='abc!1234',
            )
            self.assertEqual(user.email, expected_email)

    def test_new_user_email_required(self):
        """Test if email was provided for user."""

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email='',
                password='abc!123',
            )

    def test_create_superuser(self):
        """Test superuser creation."""
        email = 'test@test.com'
        password = 'abc1233456'
        user = get_user_model().objects.create_superuser(
            email=email,
            password=password,
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_forest_successful(self):
        """Test a successful attempt to create a forest."""
        domain = DomainsType.MATA_ATLANTICA.value
        forest = models.Forest.objects.create(name='Forest X',
                                              domain=domain)
        self.assertEqual(str(forest), forest.name)
