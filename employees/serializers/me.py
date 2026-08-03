from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from employees.models import Employee
from employees.serializers.department import EmployeeDepartmentSerializer


class EmployeeMeSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    birth_date = serializers.DateField(read_only=True)
    gender = serializers.ChoiceField(choices=Employee.Gender.choices, read_only=True)
    department = EmployeeDepartmentSerializer(read_only=True)
    employment_type = serializers.ChoiceField(
        choices=Employee.EmploymentType.choices, read_only=True
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

    current_password = serializers.CharField(
        write_only=True,
        required=False,
        allow_null=True,
        allow_blank=True,
    )
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        max_length=16,
        required=False,
        allow_null=True,
        allow_blank=True,
    )

    def validate(self, attrs):
        user = self.instance.user if self.instance else None
        password = attrs.get("password")
        current_password = attrs.get("current_password")

        if password:
            if user is None:
                raise ValidationError({"password": "Employee doesn't own an account."})
            if not current_password:
                raise ValidationError(
                    {
                        "current_password": "Current password is required to change password."
                    }
                )
            if not user.check_password(current_password):
                raise ValidationError(
                    {"current_password": "Incorrect current password."}
                )
            try:
                validate_password(password, user)
            except DjangoValidationError as e:
                raise ValidationError({"password": e.messages})
        elif current_password and not password:
            raise ValidationError(
                {
                    "password": "New password is required when current password is provided."
                }
            )

        return attrs

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        validated_data.pop("current_password", None)

        if password and instance.user:
            instance.user.set_password(password)
            instance.user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance
