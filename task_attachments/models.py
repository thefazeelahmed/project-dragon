from django.db import models

from attachments.models import Attachment
from tasks.models import Task

# Create your models here.
class TaskAttachment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE,
        related_name="task_attachments"
    )
    attachment = models.ForeignKey(Attachment, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.attachment.file.name