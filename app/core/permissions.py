from rest_framework.permissions import BasePermission


class CheckPermissions(BasePermission):
    """
    Custom permission to check user's permissions
    on the viewsets.
    """

    def has_permission(self, request, view):
        if (view.action in ('list', 'retrieve')
                or request.user.is_staff or request.user.is_superuser):
            return True
        else:
            return False
