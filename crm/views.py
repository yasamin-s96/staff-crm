from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import CreateView, DetailView, ListView

from crm.forms import EmployeeForm, UserForm, UserUpdateForm
from crm.models import Employee


class EmployeeCreateView(PermissionRequiredMixin, View):
    permission_required = "crm.create_employee"

    def get(self, request, *args, **kwargs):
        employee_form = EmployeeForm()
        user_form = UserForm()
        return render(
            request,
            "crm/employee_form.html",
            context={"form": employee_form, "user_form": user_form},
        )

    def post(self, request, *args, **kwargs):
        employee_form = EmployeeForm(request.POST)
        user_form = UserForm(request.POST)
        if employee_form.is_valid() and user_form.is_valid():
            with transaction.atomic():
                user = user_form.save()
                employee = employee_form.save(commit=False)
                employee.user = user
                employee.save()
            return redirect("crm:home")

        return render(
            request,
            "crm/employee_form.html",
            context={"form": employee_form, "user_form": user_form},
        )


class EmployeeUpdateView(PermissionRequiredMixin, View):
    permission_required = "crm.change_employee"

    def get_object(self):
        pk = self.kwargs.get("pk")
        employee = get_object_or_404(Employee, pk=pk)
        return employee

    def get(self, request, *args, **kwargs):
        employee = self.get_object()
        employee_form = EmployeeForm(instance=employee)
        user_form = UserUpdateForm(
            instance=employee.user,
        )
        return render(
            request,
            "crm/employee_update.html",
            context={"form": employee_form, "user_form": user_form},
        )

    def post(self, request, *args, **kwargs):
        employee = self.get_object()
        if employee.user == request.user:
            raise ValueError(
                "You're not allowed to make changes to your profile from this address!"
            )
        employee_form = EmployeeForm(instance=employee, data=request.POST)
        user_form = UserUpdateForm(instance=employee.user, data=request.POST)
        if employee_form.is_valid() and user_form.is_valid():
            with transaction.atomic():
                user_form.save()
                employee_form.save()
            return redirect("crm:home")

        return render(
            request,
            "crm/employee_update.html",
            context={"form": employee_form, "user_form": user_form},
        )


class EmployeeListView(LoginRequiredMixin, ListView):
    model = Employee
    template_name = "crm/home.html"

    def get_queryset(self):
        return Employee.objects.exclude(user=self.request.user)


class EmployeeDetailView(LoginRequiredMixin, DetailView):
    model = Employee
    template_name = "crm/employee_profile.html"


class EmployeeDeactivateView(PermissionRequiredMixin, View):
    permission_required = "crm.deactivate_employee"

    def post(self, request, *args, **kwargs):
        employee = get_object_or_404(Employee, pk=self.kwargs["pk"])
        if employee.user == self.request.user:
            raise ValueError(
                "You are not allowed to deactivate your account from this address!"
            )
        employee.user.is_active = False
        employee.user.save(update_fields=["is_active"])
        return redirect("crm:profile", pk=employee.pk)
