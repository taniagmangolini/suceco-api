"""Serializers for Forest API."""
from rest_framework import serializers

from core.models import Forest

from utils import fields

from utils.constants import DomainType


class ForestSerializer(serializers.ModelSerializer):
    domain = fields.EnumField(enum=DomainType)

    class Meta:
        model = Forest
        fields = ['name', 'domain']
        read_only_fields = ['id']


class ForestDetailSerializer(ForestSerializer):

    class Meta(ForestSerializer.Meta):
        fields = ForestSerializer.Meta.fields + ['is_active']
