from rest_framework.permissions import SAFE_METHODS, BasePermission


class CanManageEmployeesOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if request.method in SAFE_METHODS:
            if request.method == "GET" and "show_terminated" in request.query_params:
                return user.has_perm("view_terminated_employee")
            return True

        if request.method == "POST":
            return user.has_perm("add_employee")

        if request.method in ["PATCH", "PUT"]:
            return user.has_perm("change_employee")

        return False

    def has_object_permission(self, request, view, obj):
        user = request.user
        employee_user = obj.user
        is_manager = request.user.groups.filter(name="manager").exists()

        if is_manager:
            return obj.department.manager == user and employee_user != user

        return employee_user != user


class CanTerminateEmployee(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm("terminate_employee")

    def has_object_permission(self, request, view, obj):
        user = request.user
        employee_user = obj.user
        is_manager = request.user.groups.filter(name="manager").exists()

        if is_manager:
            return obj.department.manager == user and employee_user != user

        return employee_user != user


class CanManageSystemAccess(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return request.user.has_perms(
            [
                "change_user",
                "add_user",
            ]
        )

    def has_object_permission(self, request, view, obj):
        return True
