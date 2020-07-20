from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
        Only allow the owner of an element to edit, other users can just read it
    """
    def has_object_permission(self, request, view, obj):
        """
            Return true if the current user is the owner of the object
        """
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user
