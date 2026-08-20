from django.db import models

from attachments.models import Attachment
from projects.models import Project

# Create your models here.
class ProjectAttachment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE,
        related_name="project_attachments"
    )
    attachment = models.ForeignKey(Attachment, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.project.name