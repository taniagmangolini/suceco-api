"""
Views for the User API.
"""
from rest_framework import generics
from user.serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated


class CreateUserView(generics.CreateAPIView):
    """Create a new user."""
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
