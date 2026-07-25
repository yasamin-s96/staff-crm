from rest_framework import serializers

from departments.models import Department
from employees.models import Employee


class DepartmentSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(required=False, default=True)
    manager_id = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), required=False, allow_null=True
    )
    parent_department_id = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(), required=False, allow_null=True
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
