from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken,
)

from accounts.models import User


def blacklist_user_tokens(user: User) -> None:
    """Blacklist all outstanding refresh tokens for the given user."""
    tokens = OutstandingToken.objects.filter(user=user)
    for token in tokens:
        BlacklistedToken.objects.get_or_create(token=token)
