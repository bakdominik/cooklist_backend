from rest_framework import permissions


class RecipePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == "create":
            return request.user.is_authenticated
        else:
            return True

    def has_object_permission(self, request, view, obj):
        if view.action == "retrieve":
            return True
        if not request.user.is_authenticated:
            return False
        elif view.action in ["update", "partial_update", "destroy"]:
            return obj.owner == request.user or request.user.is_admin
        else:
            return False


class OwnerCanDeleteAuthenticatedUserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ("create", "list", "destroy", "retrieve"):
            return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        elif view.action == "destroy":
            return obj.owner == request.user or request.user.is_admin
        else:
            return False
