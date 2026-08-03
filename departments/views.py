from rest_framework import generics, viewsets

from departments.models import Department
from departments.serializers import (
    DepartmentEmployeeListSerializer,
    DepartmentSerializer,
)


class DepartmentViewSet(viewsets.ModelViewSet):
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()


class DepartmentEmployeeListView(generics.RetrieveAPIView):
    queryset = Department.objects.prefetch_related("employees")
    serializer_class = DepartmentEmployeeListSerializer
