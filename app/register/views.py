"""Views for Reference APIs."""
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)
from rest_framework import viewsets

from core.models import Register
from core.permissions import CheckPermissions

from register import serializers


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'forests',
                OpenApiTypes.STR,
                description='Comma separated forest ids to filter',
            ),
            OpenApiParameter(
                'stages',
                OpenApiTypes.STR,
                description='Comma separated stages ids to filter',
            ),
            OpenApiParameter(
                'species',
                OpenApiTypes.STR,
                description='Comma separated species ids to filter',
            ),
            OpenApiParameter(
                'states',
                OpenApiTypes.STR,
                description='Comma separated states ids to filter',
            ),
        ]
    )
)
class RegisterViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.RegisterDetailSerializer
    queryset = Register.objects.all()
    permission_classes = (CheckPermissions,)

    def _params_to_ints(self, qs):
        """Convert a lista of strings to a list of integers."""
        return [int(str_id) for str_id in qs.split(',')]

    def get_querysetx(self):
        """Retrieve active registers according to filters."""
        return self.queryset.filter(is_active=True).order_by('-id')

    def get_queryset(self):
        """Retrieve active registers according to filters."""
        forests = self.request.query_params.get('forests')
        stages = self.request.query_params.get('stages')
        species = self.request.query_params.get('species')
        states = self.request.query_params.get('states')
        queryset = self.queryset
        if forests:
            forests_ids = self._params_to_ints(forests)
            queryset = queryset.filter(forest__id__in=forests_ids)
        if stages:
            stages_values = self._params_to_ints(stages)
            queryset = queryset.filter(stage__in=stages_values)
        if species:
            species_ids = self._params_to_ints(species)
            queryset = queryset.filter(species__id__in=species_ids)
        if states:
            states_values = self._params_to_ints(states)
            queryset = queryset.filter(state__in=states_values)
        return queryset.filter(is_active=True).order_by('-id')

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.RegisterSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new register."""
        serializer.is_valid(raise_exception=True)
        serializer.save()
