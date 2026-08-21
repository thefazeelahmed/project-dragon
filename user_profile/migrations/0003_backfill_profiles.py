from django.conf import settings
from django.db import migrations


def backfill_missing_profiles(apps, schema_editor):
    User = apps.get_model("user", "User")
    UserProfile = apps.get_model("user_profile", "UserProfile")

    existing = set(UserProfile.objects.values_list("user_id", flat=True))
    to_create = [
        UserProfile(user_id=user.id, bio="")
        for user in User.objects.all()
        if user.id not in existing
    ]
    UserProfile.objects.bulk_create(to_create)


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("user_profile", "0002_alter_userprofile_user_one_to_one"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RunPython(backfill_missing_profiles, noop_reverse),
    ]
