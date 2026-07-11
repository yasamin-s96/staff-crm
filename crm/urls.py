from django.urls import path

from crm import views

app_name = "crm"

urlpatterns = [
    path("home/", views.EmployeeListView.as_view(), name="home"),
    path("employees/<int:pk>/", views.EmployeeDetailView.as_view(), name="profile"),
    path("employees/<int:pk>/update/", views.EmployeeUpdateView.as_view(), name="employee_update"),
    path("employees/<int:pk>/deactivate/", views.EmployeeDeactivateView.as_view(), name="employee_deactivate"),
    path("employees/", views.EmployeeCreateView.as_view(), name="employee_create")
]