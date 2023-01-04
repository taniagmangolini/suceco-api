"""Views for Forest APIs."""
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core.models import Forest
from forest import serializers

from utils.constants import StatusType


class ForestViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ForestSerializer
    queryset = Forest.objects.all()
    permission_classes = (AllowAny,)

    def get_queryset(self):
        """Retrieve active forests."""
        return self.queryset.filter(status=StatusType.active).order_by('-id')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)
