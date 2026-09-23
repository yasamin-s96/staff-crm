from rest_framework.permissions import BasePermission


class CanManageImportJob(BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return request.user.has_perm("view_employeeimportjob")

        else:
            return request.user.has_perm("import_employee")
