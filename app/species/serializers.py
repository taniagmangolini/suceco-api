"""Serializers for Species API."""
from rest_framework import serializers

from core.models import Species


class SpeciesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Species
        fields = ['scientific_name']
        read_only_fields = ['id']


class SpeciesDetailSerializer(SpeciesSerializer):

    class Meta(SpeciesSerializer.Meta):
        fields = SpeciesSerializer.Meta.fields + ['is_active']
