from django.urls import path

from employee_imports import views

urlpatterns = [
    path("", views.EmployeeImportJobListCreateView.as_view()),
    path("<int:pk>/items/", views.EmployeeImportJobItemsView.as_view()),
]
