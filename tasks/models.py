from django.conf import settings
from django.db import models

from projects.models import Project


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    # Many tasks per project; each task belongs to exactly one project (FK, not OneToOne)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="tasks",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tasks",
    )
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
