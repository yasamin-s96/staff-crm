from django.db.models import Q
from django.db.models.aggregates import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from auditlogs.mixins import AuditLogMixin
from employee_imports.filters import JobItemFilter
from employee_imports.models import EmployeeImportJob, ImportJobItem
from employee_imports.permissions import (
    CanManageImportJob,
)
from employee_imports.serializers import (
    EmployeeImportJobSerializer,
    EmployeeImportSerializer,
    ImportJobItemSerializer,
)


class EmployeeImportJobListCreateView(AuditLogMixin, generics.ListCreateAPIView):
    permission_classes = (CanManageImportJob,)

    def get_queryset(self):
        return EmployeeImportJob.objects.annotate(
            total_count=Count("items"),
            error_count=Count(
                "items", filter=Q(items__status=ImportJobItem.Status.ERROR)
            ),
            success_count=Count(
                "items", filter=Q(items__status=ImportJobItem.Status.ADDED)
            ),
            skipped_count=Count(
                "items", filter=Q(items__status=ImportJobItem.Status.SKIPPED)
            ),
        )

    def get_serializer_class(self):
        if self.request.method == "GET":
            return EmployeeImportJobSerializer

        else:
            return EmployeeImportSerializer


class EmployeeImportJobItemsView(generics.ListAPIView):
    serializer_class = ImportJobItemSerializer
    permission_classes = (IsAuthenticated, CanManageImportJob)
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = JobItemFilter

    def get_queryset(self):
        job_id = self.kwargs["pk"]
        queryset = ImportJobItem.objects.filter(job_id=job_id).order_by("row_number")
        return queryset
