from django.db import models

from projects.models import Project

# Create your models here.
class ProjectAttachment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    attachment = models.FileField(upload_to='project_attachments/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.project.name