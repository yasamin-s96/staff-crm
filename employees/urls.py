from django.urls import path

from employees import views

urlpatterns = [
    path("", views.EmployeeListCreateView.as_view()),
    path(
        "<int:pk>/",
        views.EmployeeRetrieveUpdateView.as_view(),
    ),
    path(
        "<int:pk>/account",
        views.AuthCredentialsUpsertView.as_view(),
    ),
]
