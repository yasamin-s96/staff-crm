from django.urls import path
from rest_framework.routers import DefaultRouter

from employees import views

app_name = "employees"

router = DefaultRouter()

test = router.register()

urlpatterns = [
    path("employees/", views.EmployeeListCreateView.as_view()),
    path(
        "employees/<int:pk>/",
        views.EmployeeRetrieveUpdateView.as_view(),
    ),
    path(
        "employees/<int:pk>/account",
        views.AuthCredentialsUpsertView.as_view(),
    ),
]
