from rest_framework.permissions import BasePermission, IsAdminUser


class IsOwnerOrAdmin(BasePermission):
    message = "You do not have permission to view this"

    def has_object_permission(self, request, view, obj):
        return obj.owner == (request.user or IsAdminUser)
