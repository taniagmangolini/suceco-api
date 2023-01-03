"""
Serializers for the User API view.
"""
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object.
    For security reasons, the password cannot be read.
    """

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name', 'last_login']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}

    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        return get_user_model().objects.create_user(**validated_data)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom TokenObtainPairSerializer
    to add custom claim (name) to the token.
    (See in the docs: customizing_token_claims)."""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['name'] = user.name
        return token


class PasswordResetEmailSerializer(serializers.Serializer):
    """Sends to the user an email with a link to change
    the password."""
    email = serializers.EmailField()

    class Meta:
        fields = ['email']


class RequestPasswordResetEmailSerializer(PasswordResetEmailSerializer):
    """Sends to the user an email with a link to change
    the password."""

    def validate_email(self, email):
        user = get_user_model().objects.filter(email=email)
        if not user:
            raise serializers.ValidationError('E-mail not found.')
        return email


class ConfirmPasswordResetSerializer(PasswordResetEmailSerializer):
    """Confirm password reset by the link received throught e-mail API"""
    token = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = ['email', 'token']


class CompletePasswordResetSerializer(ConfirmPasswordResetSerializer):
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        fields = ['password', 'token', 'email']

    def validate(self, attrs):
        try:
            new_password = attrs.get('password')
            token = attrs.get('token')
            email = attrs.get('email')
            user = get_user_model().objects.filter(email=email).first()

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError('Invalid link.')

            user.set_password(new_password)
            user.save()
        except Exception as e:
            raise serializers.ValidationError(f'[Error] {e}')

        return super().validate(attrs)
