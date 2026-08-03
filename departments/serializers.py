from rest_framework import serializers

from departments.models import Department
from employees.models import Employee
from employees.serializers import UserSerializer


class EmployeeListDisplaySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    birth_date = serializers.DateField()
    gender = serializers.ChoiceField(choices=Employee.Gender.choices)
    auth_credentials = UserSerializer(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    is_active = serializers.BooleanField(
        required=False, default=False, allow_null=False
    )


class DepartmentSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(required=False, default=True)
    manager_id = serializers.PrimaryKeyRelatedField(
        source="manager",
        queryset=Employee.objects.all(),
        required=False,
        allow_null=True,
    )
    parent_department_id = serializers.PrimaryKeyRelatedField(
        source="parent_department",
        queryset=Department.objects.all(),
        required=False,
        allow_null=True,
    )
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Department
        fields = (
            "id",
            "name",
            "description",
            "manager_id",
            "parent_department_id",
            "is_active",
            "created_at",
            "updated_at",
        )


class DepartmentEmployeeListSerializer(serializers.ModelSerializer):
    employees = EmployeeListDisplaySerializer(many=True, read_only=True)

    class Meta:
        model = Department
        fields = ("id", "name", "employees")
