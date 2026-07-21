from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from employees.models import User


class UserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        max_length=16,
        required=False,
        allow_null=False,
    )

    def validate(self, attrs):
        user = self.instance
        password = attrs.get("password")

        if user is None and password is None:
            raise ValidationError("Password is a required field for account creation.")

        if password is not None:
            try:
                validate_password(password, user)
            except DjangoValidationError as e:
                raise ValidationError({"password": e.messages})

        return attrs

    def create(self, validated_data):
        try:
            user = User.objects.create_user(**validated_data)
        except DjangoValidationError as e:
            raise ValidationError(e.message_dict)

        employee = self.context["employee"]
        employee.user = user
        employee.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.get("password")
        email = validated_data.get("email")
        instance.email = email

        if password:
            instance.set_password(password)

        try:
            instance.full_clean()
        except DjangoValidationError as e:
            raise ValidationError(e.message_dict)

        instance.save()
        return instance
