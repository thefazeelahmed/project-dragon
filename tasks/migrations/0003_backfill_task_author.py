from django.conf import settings
from django.db import migrations


def backfill_task_authors(apps, schema_editor):
    Task = apps.get_model("tasks", "Task")
    User = apps.get_model("user", "User")

    first_user = User.objects.order_by("id").first()
    if first_user is None:
        Task.objects.all().delete()
        return

    # Prefer project author when available
    for task in Task.objects.filter(author__isnull=True).select_related("project"):
        author_id = getattr(task.project, "author_id", None) or first_user.id
        task.author_id = author_id
        task.save(update_fields=["author_id"])


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("tasks", "0002_task_author"),
        ("projects", "0005_alter_project_author_organization"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RunPython(backfill_task_authors, noop_reverse),
    ]
