from rest_framework import permissions

from django.contrib.auth import get_user_model


User = get_user_model()


class AdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff or request.user.role == 'admin'
