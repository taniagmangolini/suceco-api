"""Views for Reference APIs."""
from rest_framework import viewsets

from core.models import Register
from core.permissions import CheckPermissions
from register import serializers


class RegisterViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.RegisterDetailSerializer
    queryset = Register.objects.all()
    permission_classes = (CheckPermissions,)

    def get_queryset(self):
        """Retrieve active register."""
        return self.queryset.filter(is_active=True).order_by('-id')

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.RegisterSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new register."""
        serializer.is_valid(raise_exception=True)
        serializer.save()
