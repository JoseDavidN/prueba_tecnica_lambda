from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """
    Permiso personalizado para solo permitir acceso a usuarios con el rol 'admin'.
    """

    def has_permission(self, request, view):
        # Verifica si el usuario autenticado tiene el rol 'admin'
        if request.user.is_authenticated and request.user.rol == 'admin':
            return True
        return False
