from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import AuditLog

User = get_user_model()


class ActorSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="employee.first_name")
    last_name = serializers.CharField(source="employee.last_name")

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name"]


class AuditLogSerializer(serializers.ModelSerializer):
    actor = ActorSerializer(read_only=True)

    class Meta:
        model = AuditLog
        fields = "__all__"
