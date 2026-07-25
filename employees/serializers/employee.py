from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from accounts.models import User
from departments.models import Department
from employees.models import Employee
from employees.serializers.department import EmployeeDepartmentSerializer
from employees.serializers.user import UserSerializer as UserCreateSerializer


class EmployeeSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    birth_date = serializers.DateField()
    gender = serializers.ChoiceField(choices=Employee.Gender.choices)
    auth_credentials = UserCreateSerializer(required=False)
    department = EmployeeDepartmentSerializer(read_only=True)
    department_id = serializers.PrimaryKeyRelatedField(
        source="department", queryset=Department.objects.all(), write_only=True
    )
    created_at = serializers.DateTimeField(read_only=True)
    is_active = serializers.BooleanField(
        required=False, default=False, allow_null=False
    )

    def create(self, validated_data):
        auth_credentials = validated_data.pop("auth_credentials", None)
        is_active = validated_data.pop("is_active", False)
        user = None
        if auth_credentials:
            auth_credentials.update({"is_active": is_active})
            user = User.objects.create_user(**auth_credentials)
        employee = Employee.objects.create(user=user, **validated_data)
        return employee


class EmployeeUpdateSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100, required=False, allow_null=False)
    last_name = serializers.CharField(max_length=100, required=False, allow_null=False)
    birth_date = serializers.DateField(required=False, allow_null=False)
    gender = serializers.ChoiceField(
        choices=Employee.Gender.choices,
        required=False,
        allow_null=False,
    )
    department_id = serializers.IntegerField(required=False, allow_null=False)
    is_active = serializers.BooleanField(required=False, allow_null=False)

    def validate_is_active(self, value):
        user = self.instance.user
        is_active = value
        if user is None and is_active is not None:
            raise ValidationError(
                "Employee doesn't own an account. Activation/Deactivation aborted."
            )

    def update(self, instance, validated_data):
        is_active = validated_data.pop("is_active", None)
        employee = instance
        user = employee.user
        if user is not None and is_active is not None:
            user.is_active = is_active
            user.save()

        if validated_data:
            for attr, value in validated_data.items():
                setattr(employee, attr, value)
            employee.save()

        return employee
