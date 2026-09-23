import django_filters

from .models import AuditLog


class AuditLogFilter(django_filters.FilterSet):
    occurred_at = django_filters.DateFromToRangeFilter()

    class Meta:
        model = AuditLog
        fields = {
            "actor": ["exact"],
            "action": ["exact", "iexact"],
            "object_id": ["exact"],
            "content_type": ["exact"],
        }
