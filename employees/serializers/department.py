from rest_framework import serializers

from departments.models import Department


class EmployeeDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = (
            "id",
            "name",
        )
