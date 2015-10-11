from rest_framework import permissions


class ReadAllWriteOnlyAdminPermission(permissions.BasePermission):
    """
    This function returns True for all GET requests if the user is logged in and 
    for POST requests it checks if the user is Django admin.
    """
    def has_permission(self, request, view):
        if request.method == 'GET' and request.user.is_authenticated():
            return True
        elif request.user.is_authenticated() and request.user.is_staff:
            return True
        return False