import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


def dedupe_profiles(apps, schema_editor):
    UserProfile = apps.get_model("user_profile", "UserProfile")
    seen = set()
    for profile in UserProfile.objects.order_by("id"):
        if profile.user_id in seen:
            profile.delete()
        else:
            seen.add(profile.user_id)


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("user_profile", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="bio",
            field=models.TextField(blank=True, default="", max_length=500),
        ),
        migrations.RunPython(dedupe_profiles, noop_reverse),
        migrations.AlterField(
            model_name="userprofile",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="profile",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
