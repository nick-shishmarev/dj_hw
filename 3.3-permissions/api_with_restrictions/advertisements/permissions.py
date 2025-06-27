from rest_framework.permissions import BasePermission


class IsOwnerOrAdmin(BasePermission):
    """
    Allows access only to owner or admin.
    """

    def has_object_permission(self, request, view, obj):
        # return bool(request.user and request.user == obj.creator)
        return bool(request.user and (request.user == obj.creator or request.user.is_staff))
