from __future__ import absolute_import, division, print_function, unicode_literals

from rest_framework import permissions


class AdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return(
            request.method in permissions.SAFE_METHODS or
            request.user and
            request.user.is_superuser
        )
