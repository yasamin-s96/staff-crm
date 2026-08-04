from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from departments.models import Department
from employees.filters import EmployeeFilter
from employees.models import Employee
from employees.pagination import EmployeeListPagination
from employees.permissions import CanManageEmployeesOrReadOnly, CanManageSystemAccess
from employees.serializers import (
    EmployeeMeSerializer,
    EmployeeSerializer,
    EmployeeUpdateSerializer,
)
from employees.serializers.user import UserSerializer


class EmployeeMeView(generics.RetrieveUpdateAPIView):
    serializer_class = EmployeeMeSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        user = self.request.user
        if not hasattr(user, "employee") or user.employee is None:
            from rest_framework.exceptions import NotFound

            raise NotFound("Employee profile not found for current user.")
        return user.employee

    @transaction.atomic
    def perform_update(self, serializer):
        serializer.save()


class EmployeeRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Employee.objects.all()
    permission_classes = (IsAuthenticated, CanManageEmployeesOrReadOnly)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return EmployeeSerializer
        return EmployeeUpdateSerializer

    @transaction.atomic
    def perform_update(self, serializer):
        serializer.save()


class AuthCredentialsUpsertView(generics.GenericAPIView):
    serializer_class = UserSerializer
    queryset = Employee.objects.all()
    permission_classes = (IsAuthenticated, CanManageSystemAccess)

    @transaction.atomic
    def put(self, request, *args, **kwargs):
        employee = self.get_object()
        user = employee.user
        context = {**self.get_serializer_context(), "employee": employee}
        user_serializer = self.get_serializer(
            instance=user, data=request.data, context=context
        )
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()
        return Response(user_serializer.data, status=HTTP_200_OK)


class EmployeeListCreateView(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_class = EmployeeFilter
    ordering_fields = ["created_at"]
    pagination_class = EmployeeListPagination
    permission_classes = (IsAuthenticated, CanManageEmployeesOrReadOnly)

    def get_queryset(self):
        queryset = super().get_queryset()
        department_id = self.request.query_params.get("department")
        if department_id:
            try:
                department_id = int(department_id)
            except ValueError:
                department_id = None

        include_children = self.request.query_params.get("include_children") == "true"

        if department_id:
            department_ids = [department_id]
            if include_children:
                department = Department.objects.get(pk=department_id)
                department_ids.extend(
                    self._get_sub_departments(parent_department=department)
                )
            queryset = queryset.filter(department_id__in=department_ids)

        return queryset

    @transaction.atomic
    def perform_create(self, serializer):
        serializer.save()

    def _get_sub_departments(self, parent_department):
        sub_departments = parent_department.sub_departments.all()
        sub_ids = []

        for dep in sub_departments:
            sub_ids.append(dep.id)
            sub_ids.extend(self._get_sub_departments(dep))

        return sub_ids
