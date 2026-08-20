from django.db import models

from user_profile.models import UserProfile

# Create your models here.
class UserProfileAttachment(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    attachment = models.FileField(upload_to='attachments/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user_profile.user.name