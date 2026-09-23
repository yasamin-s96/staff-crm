from django.urls import path

from employees import views

urlpatterns = [
    path("", views.EmployeeListCreateView.as_view()),
    path("me/", views.EmployeeMeView.as_view(), name="employee-me"),
    path(
        "<int:pk>/",
        views.EmployeeRetrieveUpdateView.as_view(),
    ),
    path(
        "<int:pk>/terminate/",
        views.EmployeeTerminateView.as_view(),
    ),
    path(
        "<int:pk>/account",
        views.AuthCredentialsUpsertView.as_view(),
    ),
]
