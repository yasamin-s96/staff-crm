from django.db.migrations import swappable_dependency
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User


class DepartmentAPITest(APITestCase):
    def setUp(self):
        auth_credentials = {"email": "test@example.com", "password": "test"}
        User.objects.create_user(**auth_credentials)

        response = self.client.post(reverse("token_obtain_pair"), data=auth_credentials)
        self.access_token = response.context.get("access")

    def test_departments_list(self):
        # Test unauthenticated request
        response = self.client.get(reverse("department-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
