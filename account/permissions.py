from rest_framework.permissions import BasePermission, IsAdminUser


class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (obj.owner == request.user) or IsAdminUser
