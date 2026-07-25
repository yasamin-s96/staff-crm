from rest_framework import viewsets

from departments.models import Department
from departments.serializers import DepartmentSerializer


class DepartmentViewSet(viewsets.ModelViewSet):
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()
