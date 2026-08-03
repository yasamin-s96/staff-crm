from http.client import responses

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from accounts.models import User


class DepartmentAPITest(APITestCase):
    def setUp(self):
        auth_credentials = {"email": "test@example.com", "password": "test"}
        self.bare_minimum_access_user = User.objects.create_user(**auth_credentials)

        response = self.client.post(reverse("token_obtain_pair"), data=auth_credentials)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.bare_minimum_access_token = response.data.get("access")

    def test_departments_list(self):
        self._test_auth(url_name="department-list")

    def test_department_create(self):
        data = {
            "name": "Engineering",
            "description": "testing",
        }
        self._test_auth(
            url_name="department-list",
            method="post",
            data=data,
            expected_status=status.HTTP_201_CREATED,
        )

    def _get_headers(self, token=None, **kwargs):
        token = token or self.bare_minimum_access_token
        return {"Authorization": f"Bearer {token}", **kwargs}

    def _test_auth(self, url_name, method="get", data=None, expected_status=status.HTTP_200_OK):
        # Test unauthenticated request
        url = reverse(url_name)
        response = getattr(self.client, method, "get")(url, data=data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authenticated request
        headers = self._get_headers()
        response = getattr(self.client, method, "get")(url, data=data, headers=headers)
        print(response.data)
        self.assertEqual(response.status_code, expected_status)

