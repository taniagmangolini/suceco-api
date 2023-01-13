"""Serializers for Register API."""
from rest_framework import serializers

from core.models import Register

from utils import fields
from utils.constants import StateType, StageType


class RegisterSerializer(serializers.ModelSerializer):
    stage = fields.EnumField(enum=StateType)
    state = fields.EnumField(enum=StageType)

    class Meta:
        model = Register
        fields = ['species',
                  'forest',
                  'reference',
                  'latitude',
                  'longitude',
                  'stage',
                  'state']
        read_only_fields = ['id']


class RegisterDetailSerializer(RegisterSerializer):

    class Meta(RegisterSerializer.Meta):
        fields = RegisterSerializer.Meta.fields + ['is_active',
                                                   'created_at',
                                                   'updated_at']
