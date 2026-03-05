# inventory/permissions.py
from rest_framework import permissions

class IsSeller(permissions.BasePermission):
    """
    Allows access only to users with the 'seller' role.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'seller')