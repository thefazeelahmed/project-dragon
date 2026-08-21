import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


def assign_organization_authors(apps, schema_editor):
    Organization = apps.get_model("organizations", "Organization")
    User = apps.get_model("user", "User")

    first_user = User.objects.order_by("id").first()
    if first_user is None:
        # No users yet — drop orphan orgs so non-null constraint can apply
        Organization.objects.all().delete()
        return

    Organization.objects.filter(author__isnull=True).update(author_id=first_user.id)


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("organizations", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="organization",
            name="author",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="organizations",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.RunPython(assign_organization_authors, noop_reverse),
        migrations.AlterField(
            model_name="organization",
            name="author",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="organizations",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
