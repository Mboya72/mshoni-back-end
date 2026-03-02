from rest_framework.permissions import BasePermission

class IsTailor(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "tailor"

class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "customer"

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user