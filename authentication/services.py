from authentication.models import EmailVerification
from authentication.tokens import generate_raw_token, get_token_expiry, hash_token


def create_verification_token(user, purpose: str, hours: int = 24) -> str:
    """Invalidate old unused tokens for this purpose, create a new hashed one."""
    EmailVerification.objects.filter(
        user=user,
        purpose=purpose,
        is_used=False,
    ).update(is_used=True)

    raw_token = generate_raw_token()
    EmailVerification.objects.create(
        user=user,
        token_hash=hash_token(raw_token),
        purpose=purpose,
        expires_at=get_token_expiry(hours=hours),
    )
    return raw_token
