from rest_framework import permissions

from users.models import User


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_staff or request.user.role == User.UserRoles.ADMIN


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user.is_staff or request.user.role == User.UserRoles.ADMIN
        return False


class IsOwnerOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.author or request.method in permissions.SAFE_METHODS


class IsAdminOrModOrAuthor(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        is_staff_or_owner = (
                request.user.is_authenticated and (
                request.user.is_staff or
                request.user.role == User.UserRoles.ADMIN or
                request.user.role == User.UserRoles.MODERATOR or
                obj.author == request.user
        ))

        return is_staff_or_owner or request.method in permissions.SAFE_METHODS
