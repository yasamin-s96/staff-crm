from rest_framework import generics, viewsets

from auditlogs.mixins import AuditLogMixin
from departments.models import Department
from departments.permissions import CanManageDepartments
from departments.serializers import (
    DepartmentEmployeeListSerializer,
    DepartmentSerializer,
)


class DepartmentViewSet(AuditLogMixin, viewsets.ModelViewSet):
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()
    permission_classes = [CanManageDepartments]


class DepartmentEmployeeListView(generics.RetrieveAPIView):
    queryset = Department.objects.prefetch_related("employees")
    serializer_class = DepartmentEmployeeListSerializer
