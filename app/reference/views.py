"""Views for Reference APIs."""
from rest_framework import viewsets

from core.models import Reference
from core.permissions import CheckPermissions
from reference import serializers


class ReferenceViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ReferenceDetailSerializer
    queryset = Reference.objects.all()
    permission_classes = (CheckPermissions,)

    def get_queryset(self):
        """Retrieve active reference."""
        return self.queryset.filter(is_active=True).order_by('-id')

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.ReferenceSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new reference."""
        serializer.is_valid(raise_exception=True)
        serializer.save()
