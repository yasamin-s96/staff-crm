from rest_framework import serializers

from employee_imports.models import EmployeeImportJob, ImportJobItem


class EmployeeImportSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, value):
        max_size = 5 * 1024 * 1024  # 5 MB

        if not value.name.endswith(".csv"):
            raise serializers.ValidationError("Only CSV files are accepted.")

        if value.content_type not in ("text/csv", "application/vnd.ms-excel"):
            raise serializers.ValidationError("File content type is not CSV.")

        if value.size > max_size:
            raise serializers.ValidationError("File size must not exceed 5 MB.")

        return value

    def create(self, validated_data):
        initiator = self.context["request"].user
        file = validated_data["file"]

        job = EmployeeImportJob.objects.create(file=file, initiated_by=initiator)
        return job


class EmployeeImportJobSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    status = serializers.CharField(read_only=True)
    file = serializers.FileField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    completed_at = serializers.DateTimeField(read_only=True)
    total_count = serializers.IntegerField(read_only=True)
    error_count = serializers.IntegerField(read_only=True)
    success_count = serializers.IntegerField(read_only=True)
    skipped_count = serializers.IntegerField(read_only=True)


class ImportJobItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportJobItem
        fields = ("id", "row_number", "status", "error_message", "row_data")
        read_only_fields = fields
