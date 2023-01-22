"""Serializers for Register Picture API."""
from rest_framework import serializers

from core.models import RegisterPicture


class RegisterPictureSerializer(serializers.ModelSerializer):

    class Meta:
        model = RegisterPicture
        fields = '__all__'
        read_only_fields = ['id']
        extra_kwargs = {'file': {'required': 'True'}}
