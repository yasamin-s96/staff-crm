from django.db import models
from django.db.models import Q
from django.utils import timezone

from accounts.models import User
from departments.models import Department


class Employee(models.Model):
    class Gender(models.TextChoices):
        FEMALE = "female", "Female"
        MALE = "male", "Male"

    user = models.OneToOneField(
        User, on_delete=models.PROTECT, related_name="employee", null=True
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    gender = models.CharField(choices=Gender.choices, max_length=10)
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(birth_date__lte=timezone.now().date()),
                name="not_future_birth_date",
            ),
        ]
        permissions = [("deactivate_employee", "Can deactivate employee")]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def is_active(self):
        return self.user.is_active if self.user else False
