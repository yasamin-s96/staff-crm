from django.db import transaction
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from auditlogs.mixins import AuditLogMixin
from auditlogs.models import AuditLog
from auditlogs.services import create_audit_log
from departments.models import Department
from employees.filters import EmployeeFilter
from employees.models import Employee
from employees.pagination import EmployeeListPagination
from employees.permissions import (
    CanManageEmployeesOrReadOnly,
    CanTerminateEmployee,
)
from employees.serializers import (
    EmployeeSerializer,
    EmployeeUpdateSerializer,
)


class EmployeeRetrieveUpdateView(AuditLogMixin, generics.RetrieveUpdateAPIView):
    queryset = Employee.objects.all()
    permission_classes = (IsAuthenticated, CanManageEmployeesOrReadOnly)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return EmployeeSerializer
        return EmployeeUpdateSerializer

    @transaction.atomic
    def perform_update(self, serializer):
        serializer.save()


class EmployeeTerminateView(generics.GenericAPIView):
    queryset = Employee.objects.filter(is_terminated=False)
    permission_classes = (IsAuthenticated, CanTerminateEmployee)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        employee = self.get_object()
        employee.is_terminated = True
        employee.termination_date = timezone.now()
        employee.save()

        create_audit_log(
            actor=request.user,
            action=AuditLog.Action.UPDATE,
            instance=employee,
            requested_changes={"is_terminated": True},
            final_state={
                "is_terminated": True,
                "termination_date": employee.termination_date.date().isoformat(),
            },
        )

        return Response(status=status.HTTP_204_NO_CONTENT)


class EmployeeListCreateView(AuditLogMixin, generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_class = EmployeeFilter
    ordering_fields = ["created_at"]
    pagination_class = EmployeeListPagination
    permission_classes = (IsAuthenticated, CanManageEmployeesOrReadOnly)

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.method == "GET":
            query_params = self.request.query_params
            if "show_terminated" not in query_params:
                queryset = queryset.filter(is_terminated=False)

            department_id = query_params.get("department")
            if department_id:
                try:
                    department = Department.objects.get(pk=department_id)
                except Department.DoesNotExist:
                    return queryset.none()

            include_children = query_params.get("include_children") == "true"

            if department_id:
                department_ids = [department_id]
                if include_children:
                    department_ids.extend(
                        self._get_sub_departments(parent_department=department)
                    )
                queryset = queryset.filter(department_id__in=department_ids)

        return queryset

    @transaction.atomic
    def perform_create(self, serializer):
        super().perform_create(serializer)

    def _get_sub_departments(self, parent_department):
        sub_departments = parent_department.sub_departments.all()
        sub_ids = []

        for dep in sub_departments:
            sub_ids.append(dep.id)
            sub_ids.extend(self._get_sub_departments(dep))

        return sub_ids
