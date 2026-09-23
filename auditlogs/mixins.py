from django.contrib.contenttypes.models import ContentType
from django.core.files.uploadedfile import UploadedFile

from .models import AuditLog


class AuditLogMixin:
    def _get_content_type(self, instance):
        return ContentType.objects.get_for_model(instance)

    def _make_json_serializable(self, data):
        for key, value in data.items():
            if isinstance(value, dict):
                data[key] = self._make_json_serializable(value)

            elif isinstance(value, UploadedFile):
                data[key] = {
                    "name": value.name,
                    "size": value.size,
                    "content_type": value.content_type,
                }

        return data

    def perform_create(self, serializer):
        instance = serializer.save()
        content_type = self._get_content_type(instance)
        requested_changes = self._make_json_serializable(
            serializer.validated_data.copy()
        )
        AuditLog.objects.create(
            actor=self.request.user,
            action=AuditLog.Action.CREATE,
            content_type=content_type,
            object_id=instance.id,
            requested_changes=requested_changes,
            final_state=None,
        )

    def perform_update(self, serializer):
        instance = serializer.save()
        requested_changes = self._make_json_serializable(
            serializer.validated_data.copy()
        )
        content_type = self._get_content_type(instance)

        full_final_state = serializer.data
        final_state = {
            k: full_final_state[k] for k in requested_changes if k in full_final_state
        }

        AuditLog.objects.create(
            actor=self.request.user,
            action=AuditLog.Action.UPDATE,
            content_type=content_type,
            object_id=instance.id,
            requested_changes=requested_changes,
            final_state=final_state,
        )

    def perform_destroy(self, instance):
        content_type = self._get_content_type(instance)
        object_id = instance.id
        instance.delete()
        AuditLog.objects.create(
            actor=self.request.user,
            action=AuditLog.Action.DELETE,
            content_type=content_type,
            object_id=object_id,
        )
