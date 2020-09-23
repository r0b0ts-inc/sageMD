from rest_framework.permissions import BasePermission
from rest_framework import permissions


class IsProfileOwner(BasePermission):
    message = 'Permission denied, you are not the profile owner'
    tuple_safe_methods = tuple(list(permissions.SAFE_METHODS) + ['PATCH', 'DELETE'])

    def has_object_permission(self, request, view, obj):
        if request.method not in self.tuple_safe_methods:
            return False
        return obj.user == request.user
