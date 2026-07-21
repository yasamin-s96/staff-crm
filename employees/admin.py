from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from employees.models import Employee, Department, User

class EmployeeInline(admin.StackedInline):
    model = Employee

class UserAdmin(BaseUserAdmin):
    # What columns show in the user list page
    list_display = ("email", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active", "is_superuser")
    search_fields = ("email",)
    ordering = ("email",)
    inlines = (EmployeeInline,)
    # Fields shown when EDITING an existing user
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
    # Fields shown when CREATING a new user via admin
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )


admin.site.register(User, UserAdmin)

# Register your models here.
admin.site.register(Employee)
admin.site.register(Department)
