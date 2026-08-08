from django.contrib.contenttypes.models import ContentType

from .models import AuditLog


class AuditLogMixin:
    def _get_content_type(self, instance):
        return ContentType.objects.get_for_model(instance)

    def perform_create(self, serializer):
        instance = serializer.save()
        content_type = self._get_content_type(instance)
        AuditLog.objects.create(
            actor=self.request.user,
            action=AuditLog.Action.CREATE,
            content_type=content_type,
            object_id=instance.id,
            requested_changes=serializer.validated_data,
            final_state=None,
        )

    def perform_update(self, serializer):
        requested_changes = serializer.validated_data
        instance = serializer.save()
        content_type = self._get_content_type(instance)

        full_final_state = type(serializer)(instance, context=serializer.context).data
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
