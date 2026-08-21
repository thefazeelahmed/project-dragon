from django.conf import settings
from django.db import models


class EmailVerification(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="email_verifications",
    )

    token_hash = models.CharField(max_length=128)

    purpose = models.CharField(
        max_length=30,
        default="signup",
    )

    expires_at = models.DateTimeField()

    is_used = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    used_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} - {self.purpose}"
