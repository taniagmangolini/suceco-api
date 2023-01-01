"""
Views for the User API.
"""
from rest_framework import generics
from user.serializers import UserSerializer, CustomTokenObtainPairSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView


class CreateUserView(generics.CreateAPIView):
    """Create a new user."""
    serializer_class = UserSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom CustomTokenObtainPairView."""
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = (AllowAny,)
