from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True, default="")
    manager = models.ForeignKey(
        "employees.Employee",
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET_NULL,
        related_name="managed_departments",
    )
    parent_department = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET_NULL,
        related_name="sub_departments",
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
