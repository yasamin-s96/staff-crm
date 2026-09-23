from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import AuditLog
from .permissions import CanViewAuditLog
from .serializers import AuditLogSerializer
from .filters import AuditLogFilter


class AuditLogListView(generics.ListAPIView):
    queryset = AuditLog.objects.select_related("actor", "actor__employee").order_by(
        "-occurred_at"
    )
    serializer_class = AuditLogSerializer
    permission_classes = (IsAuthenticated, CanViewAuditLog)
    filter_backends = [DjangoFilterBackend]
    filterset_class = AuditLogFilter
