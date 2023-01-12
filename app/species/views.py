"""Views for Species APIs."""
from rest_framework import viewsets

from core.models import Species
from core.permissions import CheckPermissions
from species import serializers


class SpeciesViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SpeciesDetailSerializer
    queryset = Species.objects.all()
    permission_classes = (CheckPermissions,)

    def get_queryset(self):
        """Retrieve active species."""
        return self.queryset.filter(is_active=True).order_by('-id')

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.SpeciesSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new species."""
        serializer.is_valid(raise_exception=True)
        serializer.save()
