from django.db import models
from django.db.models import Q
from django.utils import timezone


class Employee(models.Model):
    class Gender(models.TextChoices):
        FEMALE = "female", "Female"
        MALE = "male", "Male"

    class EmploymentType(models.TextChoices):
        FULL_TIME = "Full Time", "Full Time"
        PART_TIME = "Part Time", "Part Time"
        CONTRACT = "Contract", "Contract"
        INTERN = "Intern", "Intern"

    user = models.OneToOneField(
        "accounts.User", on_delete=models.PROTECT, related_name="employee", null=True
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    gender = models.CharField(choices=Gender.choices, max_length=10)
    department = models.ForeignKey(
        "departments.Department", on_delete=models.PROTECT, related_name="employees"
    )
    emergency_contact_phone = models.CharField(max_length=20, null=True, blank=True)
    emergency_contact_relationship = models.CharField(
        max_length=100, null=True, blank=True
    )
    emergency_contact_name = models.CharField(max_length=100, null=True, blank=True)
    employment_type = models.CharField(
        max_length=100,
        choices=EmploymentType.choices,
        default=EmploymentType.FULL_TIME,
    )
    termination_date = models.DateField(null=True, blank=True)
    is_terminated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(birth_date__lte=timezone.now().date()),
                name="not_future_birth_date",
            ),
        ]
        permissions = [
            ("terminate_employee", "Can terminate employee"),
            ("view_terminated_employee", "Can view terminated employee"),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def is_active(self):
        return self.user.is_active if self.user else False
