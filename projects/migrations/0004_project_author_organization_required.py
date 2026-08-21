from django.conf import settings
from django.db import migrations


def backfill_project_fields(apps, schema_editor):
    Project = apps.get_model("projects", "Project")
    Organization = apps.get_model("organizations", "Organization")
    User = apps.get_model("user", "User")

    first_user = User.objects.order_by("id").first()
    first_org = Organization.objects.order_by("id").first()

    if first_user is None or first_org is None:
        Project.objects.all().delete()
        return

    Project.objects.filter(organization__isnull=True).update(organization_id=first_org.id)
    Project.objects.filter(author__isnull=True).update(author_id=first_user.id)


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0003_project_author"),
        ("organizations", "0002_organization_author"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RunPython(backfill_project_fields, noop_reverse),
    ]
