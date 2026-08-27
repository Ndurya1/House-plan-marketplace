from rest_framework import permissions
from users.models import User


class IsSellerOwnerOrAdmin(permissions.BasePermission):
    """
    Ensures that only users with the SELLER role can create plans, 
    only the owner of the plan (linked via their SellerProfile) can edit/delete it,
    and admins have bypass privileges.
    """
    def has_permission(self, request, view):
        # Allow public read operations (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write operations (POST, PUT, PATCH, DELETE) require authentication
        if not (request.user and request.user.is_authenticated):
            return False

        # Only Admin and Seller roles are authorized to create or modify plans
        return request.user.role in [User.UserChoices.ADMIN, User.UserChoices.SELLER]

    def has_object_permission(self, request, view, obj):
        # Admins can bypass object ownership checks
        if request.user.role == User.UserChoices.ADMIN:
            return True

        # Validate that the plan's seller matches the current user
        return bool(obj.seller and obj.seller.user == request.user)
