"""Views for Forest APIs."""
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from core.models import Forest
from forest import serializers


class ForestViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ForestDetailSerializer
    queryset = Forest.objects.all()
    permission_classes = (AllowAny,)

    def get_queryset(self):
        """Retrieve active forests."""
        return self.queryset.filter(is_active=True).order_by('-id')

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.ForestSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new forest."""
        serializer.is_valid(raise_exception=True)
        serializer.save()
