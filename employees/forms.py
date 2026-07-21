from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    SetPasswordForm,
    SetPasswordMixin,
)

from employees.models import Employee, User


class UserForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        required=True,
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        required=True,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email",)


class UserUpdateForm(SetPasswordMixin, forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        required=False,
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        required=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
    )

    class Meta:
        model = User
        fields = ("email",)

    def is_password_provided(self):
        return bool(
            self.cleaned_data.get("password1")
            and self.cleaned_data.get("password2")
        )

    def clean(self):
        cleaned_data = super().clean()
        user = self.instance
        if user is None or not isinstance(user, User):
            raise ValueError("User update form requires current user instance.")

        self.validate_passwords()

        if self.is_password_provided():
            self.validate_password_for_user(user)

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.is_password_provided():
            user.set_password(raw_password=self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = (
            "first_name",
            "last_name",
            "birth_date",
            "gender",
            "department",
        )
