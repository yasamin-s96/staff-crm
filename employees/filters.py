import django_filters

from employees.models import Employee


class EmployeeFilter(django_filters.FilterSet):
    is_active = django_filters.BooleanFilter(field_name="user__is_active")
    email = django_filters.CharFilter(field_name="user__email", lookup_expr="icontains")
    first_name = django_filters.CharFilter(lookup_expr="icontains")
    last_name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Employee
        fields = ("is_active", "email", "first_name", "last_name")
