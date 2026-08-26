import csv
import io
import logging
import os
import sys
import time
from datetime import date
from typing import Annotated

import django
from django.utils import timezone
from pydantic import BaseModel, StringConstraints, ValidationError, model_validator

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

django.setup()

from departments.models import Department  # noqa: E402
from employees.models import Employee, EmployeeImportJob, ImportJobItem  # noqa: E402

logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.INFO)


StrippedName = Annotated[str, StringConstraints(min_length=2, strip_whitespace=True)]


class EmployeeRowSchema(BaseModel):
    first_name: StrippedName
    last_name: StrippedName
    birth_date: date
    gender: Employee.Gender
    employment_type: Employee.EmploymentType | None = Employee.EmploymentType.FULL_TIME
    department: StrippedName | None = None
    emergency_contact_phone: str | None = None
    emergency_contact_relationship: str | None = None
    emergency_contact_name: str | None = None

    @model_validator(mode="before")
    @classmethod
    def empty_strings_to_none(cls, values):
        return {k: (None if v == "" else v) for k, v in values.items()}


def _process_job(job: EmployeeImportJob) -> None:
    logger.info("Processing import job #%s", job.id)
    job.status = EmployeeImportJob.Status.PROCESSING
    job.save(update_fields=["status"])

    has_any_success = False

    with job.file.open("rb") as f:
        reader = csv.DictReader(io.TextIOWrapper(f, encoding="utf-8", newline=""))

        for row_number, row in enumerate(reader, start=1):
            row_data = dict(row)

            try:
                parsed = EmployeeRowSchema(**row_data)
            except ValidationError as e:
                error_msg = str(e)
                logger.warning(
                    "Job #%s row %d validation error: %s",
                    job.id,
                    row_number,
                    error_msg,
                )
                ImportJobItem.objects.create(
                    job=job,
                    row_number=row_number,
                    status=ImportJobItem.Status.ERROR,
                    error_message=error_msg,
                    row_data=row_data,
                )
                continue

            department = None
            if parsed.department:
                try:
                    department = Department.objects.get(name=parsed.department)
                except Department.DoesNotExist:
                    error_msg = f"Department '{parsed.department}' not found."
                    logger.warning("Job #%s row %d: %s", job.id, row_number, error_msg)
                    ImportJobItem.objects.create(
                        job=job,
                        row_number=row_number,
                        status=ImportJobItem.Status.ERROR,
                        error_message=error_msg,
                        row_data=row_data,
                    )
                    continue

            Employee.objects.create(
                **parsed.model_dump(exclude_none=True, exclude={"department"}),
                department=department,
            )
            has_any_success = True

            ImportJobItem.objects.create(
                job=job,
                row_number=row_number,
                status=ImportJobItem.Status.ADDED,
                row_data=row_data,
            )
            logger.info("Job #%s row %d: employee created.", job.id, row_number)

    job.completed_at = timezone.now()
    job.status = (
        EmployeeImportJob.Status.COMPLETED
        if has_any_success
        else EmployeeImportJob.Status.FAILED
    )
    job.save(update_fields=["status", "completed_at"])
    logger.info("Job #%s finished with status %s.", job.id, job.status)


def process():
    while True:
        pending_imports = list(
            EmployeeImportJob.objects.filter(status=EmployeeImportJob.Status.PENDING)
        )

        if pending_imports:
            for job in pending_imports:
                _process_job(job)
        else:
            logger.info("No pending import jobs found.")

        logger.info("Sleeping for 15 minutes...")
        time.sleep(30)


if __name__ == "__main__":
    process()
