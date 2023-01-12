"""Serializers for Reference API."""
from rest_framework import serializers

from core.models import Reference


class ReferenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reference
        fields = ['publication', 'url']
        read_only_fields = ['id']


class ReferenceDetailSerializer(ReferenceSerializer):

    class Meta(ReferenceSerializer.Meta):
        fields = ReferenceSerializer.Meta.fields + ['is_active']
