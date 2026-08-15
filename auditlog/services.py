from django.contrib.contenttypes.models import ContentType

from .models import AuditLog


def create_audit_log(
    actor,
    action,
    instance,
    requested_changes=None,
    full_final_state=None,
    final_state=None,
):
    """
    Creates an AuditLog entry for a given model instance.
    """
    content_type = ContentType.objects.get_for_model(instance)

    if requested_changes is not None:
        if full_final_state is not None and final_state is None:
            final_state = {
                k: full_final_state[k]
                for k in requested_changes
                if k in full_final_state
            }

    return AuditLog.objects.create(
        actor=actor,
        action=action,
        content_type=content_type,
        object_id=instance.pk,
        requested_changes=requested_changes,
        final_state=final_state,
    )
