import hashlib
import secrets
from datetime import timedelta

from django.utils import timezone


def generate_raw_token() -> str:
    return secrets.token_urlsafe(32)


def hash_token(raw_token: str) -> str:
    return hashlib.sha256(raw_token.encode("utf-8")).hexdigest()


def get_token_expiry(hours: int = 24):
    return timezone.now() + timedelta(hours=hours)
