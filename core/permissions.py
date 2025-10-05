from rest_framework import permissions

# This custom permission class ensures that only the user who created a booking can modify it[cite: 201].
class IsBookingOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of a booking to edit it.
    """
    # The has_object_permission method checks if the booking's user matches the request's user[cite: 203, 205].
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the booking.
        return obj.user == request.user