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
        "departments.Department",
        on_delete=models.PROTECT,
        related_name="employees",
        null=True,
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
            ("import_employee", "Can import employee"),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def is_active(self):
        return self.user.is_active if self.user else False


class EmployeeImportJob(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PROCESSING = "PROCESSING", "Processing"
        COMPLETED = "COMPLETED", "Completed"
        FAILED = "FAILED", "Failed"

    file = models.FileField(upload_to="employee_imports/")
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True,
    )
    initiated_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.PROTECT,
        related_name="employee_import_jobs",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Import Job #{self.id} - {self.get_status_display()}"


class ImportJobItem(models.Model):
    class Status(models.TextChoices):
        ADDED = "ADDED", "Added"
        SKIPPED = "SKIPPED", "Skipped"
        ERROR = "ERROR", "Error"

    job = models.ForeignKey(
        EmployeeImportJob,
        on_delete=models.CASCADE,
        related_name="items",
    )
    row_number = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        db_index=True,
    )
    error_message = models.TextField(blank=True)
    row_data = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"Job {self.job_id} Item {self.row_number} - {self.get_status_display()}"
