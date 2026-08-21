from django.conf import settings
from django.core.mail import send_mail


def _send(user, subject: str, body: str) -> None:
    send_mail(
        subject=subject,
        message=body,
        from_email=getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@example.com"),
        recipient_list=[user.email],
        fail_silently=False,
    )


def send_verification_email(user, raw_token: str) -> None:
    verify_url = f"{settings.FRONTEND_URL}/auth/email/verify/"
    body = (
        f"Hi {user.name},\n\n"
        f"Use this token to verify your email:\n\n"
        f"{raw_token}\n\n"
        f"POST it to: {verify_url}\n\n"
        f"This token expires in 24 hours.\n"
    )
    _send(user, "Verify your email", body)


def send_password_reset_email(user, raw_token: str) -> None:
    reset_url = f"{settings.FRONTEND_URL}/auth/password/reset/"
    body = (
        f"Hi {user.name},\n\n"
        f"Use this token to reset your password:\n\n"
        f"{raw_token}\n\n"
        f"POST it to: {reset_url}\n\n"
        f"This token expires in 1 hour.\n"
    )
    _send(user, "Reset your password", body)
