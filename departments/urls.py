from django.urls import include, path
from rest_framework.routers import DefaultRouter

from departments.views import DepartmentEmployeeListView, DepartmentViewSet

router = DefaultRouter()
router.register(prefix="", viewset=DepartmentViewSet, basename="department")

urlpatterns = [
    path("", include(router.urls)),
    path("<int:pk>/employees/", DepartmentEmployeeListView.as_view()),
]
