from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    #def has_permission(self, request, view):
    #    return bool(
    #        request.method in permissions.SAFE_METHODS or
    #        request.user and
    #        request.user.is_authenticated
    #    )
    def has_object_permission(self, request, view, obj):
        return request.user == obj.author or request.method in permissions.SAFE_METHODS

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_staff or request.user.role == 'admin'


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user.is_staff or request.user.role == 'admin'
        
class IsUserModeratorAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or request.user.is_authenticated

class ModPerm(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_staff or request.auth and request.user.role == 'moderator'
    
    
class AdmPerm(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_superuser or request.auth and request.user.role == 'admin'
            

class UserPerm(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated or request.auth and request.user.role == 'user'
