from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction

from accounts.models import User
from accounts.services import blacklist_user_tokens
from auditlog.models import AuditLog
from auditlog.services import create_audit_log
from employees.models import Employee


@transaction.atomic
def update_employee_user(*, employee: Employee, validated_data, actor: User) -> User:
    """
    Application service to create or update an Employee's User account,
    manage the employee linkage, handle token invalidation upon deactivation,
    and record the audit log atomically.
    """
    user = employee.user
    action = AuditLog.Action.UPDATE if user else AuditLog.Action.CREATE

    # Record the active state prior to changes to detect deactivations
    was_active = user.is_active if user else False

    # Create or update the user model
    if user is None:
        user_instance = User.objects.create_user(**validated_data)
        employee.user = user_instance
        employee.save()

    else:
        user_instance = user
        password = validated_data.get("password")
        email = validated_data.get("email")
        is_active = validated_data.get("is_active")

        user_instance.email = email
        if is_active is not None:
            user_instance.is_active = is_active

        if password:
            user_instance.set_password(password)

        try:
            user_instance.full_clean()
        except DjangoValidationError as e:
            from rest_framework.exceptions import ValidationError

            raise ValidationError(e.message_dict)

        user_instance.save()

    # Blacklist tokens only on active -> inactive transition
    if was_active and not user_instance.is_active:
        blacklist_user_tokens(user_instance)

    # Prepare audit log requested changes, ensuring sensitive data is not exposed
    requested_changes = dict(validated_data)
    requested_changes.pop("password", None)

    full_final_state = {
        "email": user_instance.email,
        "is_active": user_instance.is_active,
    }

    create_audit_log(
        actor=actor,
        action=action,
        instance=user_instance,
        requested_changes=requested_changes,
        full_final_state=full_final_state,
    )

    return user_instance
