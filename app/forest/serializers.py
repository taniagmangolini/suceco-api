"""Serializers for Forest API."""
from rest_framework import serializers

from core.models import Forest


class ForestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Forest
        fields = ['name', 'domain']
        read_only_fields = ['id']


class ForestDetailSerializer(ForestSerializer):

    class Meta(ForestSerializer.Meta):
        fields = ForestSerializer.Meta.fields + ['status']
