from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from accounts.models import User


class UserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        max_length=16,
        required=False,
    )
    is_active = serializers.BooleanField(required=False, default=True)

    def validate(self, attrs):
        existing_user = self.instance
        password = attrs.get("password")

        if existing_user is None and password is None:
            raise ValidationError("Password is a required field for account creation.")

        if password is not None:
            try:
                validate_password(password, existing_user)
            except DjangoValidationError as e:
                raise ValidationError({"password": e.messages})

        return attrs
