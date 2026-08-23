from django.db import transaction
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from employees.models import Employee
from employees.permissions import CanManageSystemAccess
from employees.serializers import EmployeeMeSerializer
from employees.serializers.user import UserSerializer
from employees.services import update_employee_user


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


class AuthCredentialsUpsertView(generics.GenericAPIView):
    serializer_class = UserSerializer
    queryset = Employee.objects.all()
    permission_classes = (IsAuthenticated, CanManageSystemAccess)

    def put(self, request, *args, **kwargs):
        employee = self.get_object()
        user = employee.user

        user_serializer = self.get_serializer(
            instance=user,
            data=request.data,
        )
        user_serializer.is_valid(raise_exception=True)

        user_instance = update_employee_user(
            employee=employee,
            validated_data=user_serializer.validated_data,
            actor=request.user,
        )

        response_serializer = self.get_serializer(instance=user_instance)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
