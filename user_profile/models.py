from django.conf import settings
from django.db import models


class UserProfile(models.Model):
    """
    App-facing identity layer (1:1 with auth User).
    Domain FKs can stay on User for now; migrate to profile_id later if needed.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    bio = models.TextField(max_length=500, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile<{self.user.email}>"
