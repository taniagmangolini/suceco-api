"""Views for Reference APIs."""
from rest_framework import viewsets, parsers

from core.models import RegisterPicture
from core.permissions import CheckPermissions
from register_picture import serializers


class RegisterPictureViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.RegisterPictureSerializer
    queryset = RegisterPicture.objects.all()
    permission_classes = (CheckPermissions,)
    parser_classes = (parsers.FormParser, parsers.MultiPartParser)

    def get_queryset(self):
        """Retrieve active registers pictures."""
        return self.queryset.filter(is_active=True).order_by('-id')

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.RegisterPictureSerializer
        return self.serializer_class
