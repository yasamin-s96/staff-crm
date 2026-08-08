from rest_framework.permissions import BasePermission

class CanViewAuditLog(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm("auditlog.view_auditlog")
