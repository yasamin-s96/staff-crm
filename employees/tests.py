from datetime import date
from django.test import TestCase

from departments.models import Department
from employees.models import Employee


class EmployeeModelTests(TestCase):
    def setUp(self):
        self.department = Department.objects.create(
            name="HR", description="Human Resources"
        )

    def test_employee_default_employment_type_and_optional_emergency_contacts(self):
        employee = Employee.objects.create(
            first_name="Jane",
            last_name="Doe",
            birth_date=date(1990, 1, 1),
            gender=Employee.Gender.FEMALE,
            department=self.department,
        )
        self.assertEqual(employee.employment_type, Employee.EmploymentType.FULL_TIME)
        self.assertEqual(employee.employment_type, "Full Time")
        self.assertIsNone(employee.emergency_contact_phone)
        self.assertIsNone(employee.emergency_contact_relationship)
        self.assertIsNone(employee.emergency_contact_name)

    def test_employee_with_emergency_contacts(self):
        employee = Employee.objects.create(
            first_name="John",
            last_name="Smith",
            birth_date=date(1985, 5, 10),
            gender=Employee.Gender.MALE,
            department=self.department,
            employment_type=Employee.EmploymentType.PART_TIME,
            emergency_contact_phone="555-1234",
            emergency_contact_relationship="Spouse",
            emergency_contact_name="Alice Smith",
        )
        self.assertEqual(employee.employment_type, "Part Time")
        self.assertEqual(employee.emergency_contact_phone, "555-1234")
        self.assertEqual(employee.emergency_contact_relationship, "Spouse")
        self.assertEqual(employee.emergency_contact_name, "Alice Smith")


from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from accounts.models import User


class EmployeeMeAPITests(APITestCase):
    def setUp(self):
        self.department = Department.objects.create(
            name="Engineering", description="Eng Dept"
        )
        self.user_password = "OldPassword123!"
        self.user = User.objects.create_user(
            email="employee@example.com", password=self.user_password
        )
        self.employee = Employee.objects.create(
            user=self.user,
            first_name="Alice",
            last_name="Johnson",
            birth_date=date(1992, 4, 15),
            gender=Employee.Gender.FEMALE,
            department=self.department,
        )
        self.url = reverse("employee-me")

    def test_get_me_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_me_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "Alice")
        self.assertEqual(response.data["last_name"], "Johnson")

    def test_update_emergency_contacts(self):
        self.client.force_authenticate(user=self.user)
        payload = {
            "emergency_contact_name": "Bob Johnson",
            "emergency_contact_phone": "555-0000",
            "emergency_contact_relationship": "Brother",
        }
        response = self.client.patch(self.url, data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.employee.refresh_from_db()
        self.assertEqual(self.employee.emergency_contact_name, "Bob Johnson")
        self.assertEqual(self.employee.emergency_contact_phone, "555-0000")
        self.assertEqual(
            self.employee.emergency_contact_relationship, "Brother"
        )

    def test_update_password_success(self):
        self.client.force_authenticate(user=self.user)
        payload = {
            "current_password": self.user_password,
            "password": "NewSecurePassword123!",
        }
        response = self.client.patch(self.url, data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("NewSecurePassword123!"))

    def test_update_password_wrong_current_password(self):
        self.client.force_authenticate(user=self.user)
        payload = {
            "current_password": "WrongPassword!",
            "password": "NewSecurePassword123!",
        }
        response = self.client.patch(self.url, data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("current_password", response.data)


