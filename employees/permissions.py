from rest_framework.permissions import SAFE_METHODS, BasePermission


class CanManageEmployeesOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return request.user.has_perms(
            [
                "employees.change_employee",
                "employees.add_employee",
                "employees.deactivate_employee",
                "employees.view_employee",
            ]
        )

    def has_object_permission(self, request, view, obj):
        return True


class CanManageSystemAccess(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return request.user.has_perms(
            [
                "accounts.change_user",
                "accounts.add_user",
            ]
        )

    def has_object_permission(self, request, view, obj):
        return True
