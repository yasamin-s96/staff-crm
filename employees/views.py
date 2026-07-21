from django.db import transaction
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from employees.models import Employee
from employees.serializers import EmployeeSerializer, EmployeeUpdateSerializer
from employees.serializers.user import UserSerializer


class EmployeeRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Employee.objects.all()

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
    filter_backends = [OrderingFilter]
    ordering_fields = ["created_at"]

    @transaction.atomic
    def perform_create(self, serializer):
        serializer.save()
