from django.db import models
from django.db.models import Q
from django.utils import timezone


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
