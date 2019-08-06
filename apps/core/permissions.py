from rest_framework import permissions

class NoClientePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.rol == "Cliente":
            return False
        return True