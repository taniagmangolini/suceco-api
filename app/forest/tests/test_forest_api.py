"""Tests for Forest API"""
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Forest

from forest.serializers import ForestSerializer, ForestDetailSerializer

from utils.constants import DomainsType, StatusType


FOREST_URL = reverse('forest:forest-list')


def detail_url(forest_id):
    """Create and return a forest details."""
    return reverse('forest:forest-detail', args=[forest_id])


def create_forest(**params):
    """Create and return forest."""
    forest = Forest.objects.create(name=params['name'],
                                   domain=DomainsType.mata_atlantica)
    return forest


class PublicForestAPITests(TestCase):
    """Test unauthenticated forest API."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_not_required(self):
        """Test list forests."""
        create_forest(**{'name': 'Forest Test X'})
        create_forest(**{'name': 'Forest Test Y'})

        res = self.client.get(FOREST_URL)
        status_type = StatusType.active
        forests = Forest.objects.filter(status=status_type).order_by('-id')
        serializer = ForestSerializer(forests, many=True)

        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEquals(res.data, serializer.data)

    def test_get_forest_detail(self):
        """Test get forest detail."""
        forest = create_forest(**{'name': 'Forest Test W'})
        url = detail_url(forest.id)
        res = self.client.get(url)
        serializer = ForestDetailSerializer(forest)

        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEquals(res.data, serializer.data)
