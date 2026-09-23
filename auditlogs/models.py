from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models


class AuditLog(models.Model):
    class Action(models.TextChoices):
        CREATE = 'Create', 'Create'
        UPDATE = 'Update', 'Update'
        DELETE = 'Delete', 'Delete'

    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    action = models.CharField(max_length=10, choices=Action.choices)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.BigIntegerField()
    requested_changes = models.JSONField(null=True, blank=True)
    final_state = models.JSONField(null=True, blank=True)
    occurred_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.actor} {self.action} on {self.content_type} ({self.object_id})"
