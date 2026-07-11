from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import check_password, make_password
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.db.models import Q
from django.utils import timezone


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The email field must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Employee(models.Model):
    class Gender(models.TextChoices):
        FEMALE = "female", "Female"
        MALE = "male", "Male"

    # class Role(models.TextChoices):
    #     MANAGER = "manager", "Manager"
    #     STAFF = "staff", "Staff Member"

    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name="employee")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    # role = models.CharField(choices=Role.choices, max_length=50, default=Role.STAFF)
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

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
