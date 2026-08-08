from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import AuditLog
from .permissions import CanViewAuditLog
from .serializers import AuditLogSerializer


class AuditLogListAPIView(generics.ListAPIView):
    queryset = AuditLog.objects.all().order_by("-occurred_at")
    serializer_class = AuditLogSerializer
    permission_classes = (IsAuthenticated, CanViewAuditLog)
