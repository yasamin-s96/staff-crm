from rest_framework import permissions


class CanManageDepartments(permissions.BasePermission):
    """
    Allows access to authenticated users for read-only operations.
    Requires specific model permissions for write operations.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated

        # Check for model permissions
        if request.method == "POST":
            return request.user.has_perm("departments.add_department")
        if request.method in ["PUT", "PATCH"]:
            return request.user.has_perm("departments.change_department")
        if request.method == "DELETE":
            return request.user.has_perm("departments.delete_department")

        return False
