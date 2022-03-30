from rest_framework import permissions

from portal.settings import (
    BRANCH_MANAGER_LEVEL,
    CLIENT_LEVEL,
    EMPLOYEE_LEVEL,
    PORTAL_MANAGER_LEVEL,
    RESTAURANT_MANAGER_LEVEL,
)


class IsPortalManager(permissions.BasePermission):
    """Permission for Portal Manager."""

    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_authenticated and user.role.level == PORTAL_MANAGER_LEVEL
        )


class IsRestaurantManager(permissions.BasePermission):
    """Permission for Restaurant Manager."""

    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_authenticated and
            user.role.level == RESTAURANT_MANAGER_LEVEL
        )


class IsBranchManager(permissions.BasePermission):
    """Permission for Branch Manager."""

    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_authenticated and user.role.level == BRANCH_MANAGER_LEVEL
        )


class IsEmployee(permissions.BasePermission):
    """Permission for Employee."""

    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_authenticated and user.role.level == EMPLOYEE_LEVEL
        )


class IsClient(permissions.BasePermission):
    """Permission for Client."""

    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_authenticated and user.role.level == CLIENT_LEVEL
        )


class ReadOnly(permissions.BasePermission):
    """Permission to read only."""

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS