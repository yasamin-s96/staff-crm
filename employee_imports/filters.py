import django_filters

from employee_imports.models import ImportJobItem


class JobItemFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = ImportJobItem
        fields = ("status",)
