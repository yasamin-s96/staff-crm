from django.utils import timezone
from rest_framework import serializers

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
    auth_credentials = UserCreateSerializer(source="user", required=False)
    department = EmployeeDepartmentSerializer(read_only=True)
    department_id = serializers.PrimaryKeyRelatedField(
        source="department", queryset=Department.objects.all(), write_only=True
    )
    emergency_contact_phone = serializers.CharField(
        max_length=20, required=False, allow_null=True, allow_blank=True
    )
    emergency_contact_relationship = serializers.CharField(
        max_length=100, required=False, allow_null=True, allow_blank=True
    )
    emergency_contact_name = serializers.CharField(
        max_length=100, required=False, allow_null=True, allow_blank=True
    )
    employment_type = serializers.ChoiceField(
        choices=Employee.EmploymentType.choices,
        required=False,
        default=Employee.EmploymentType.FULL_TIME,
    )
    is_terminated = serializers.BooleanField(
        required=False, default=False, allow_null=False
    )
    termination_date = serializers.DateField(required=False, allow_null=True)
    created_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        auth_credentials = validated_data.pop("auth_credentials", None)
        user = None
        if auth_credentials:
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
    emergency_contact_phone = serializers.CharField(
        max_length=20, required=False, allow_null=True, allow_blank=True
    )
    emergency_contact_relationship = serializers.CharField(
        max_length=100, required=False, allow_null=True, allow_blank=True
    )
    emergency_contact_name = serializers.CharField(
        max_length=100, required=False, allow_null=True, allow_blank=True
    )
    employment_type = serializers.ChoiceField(
        choices=Employee.EmploymentType.choices,
        required=False,
        allow_null=False,
    )
    termination_date = serializers.DateField(required=False, allow_null=True)
    is_terminated = serializers.BooleanField(required=False, allow_null=False)

    def update(self, instance, validated_data):
        employee = instance

        is_terminated_req = validated_data.get("is_terminated")
        if is_terminated_req is True and not employee.is_terminated:
            if "termination_date" not in validated_data:
                validated_data["termination_date"] = timezone.now().date()

        if validated_data:
            for attr, value in validated_data.items():
                setattr(employee, attr, value)
            employee.save()

        return employee
