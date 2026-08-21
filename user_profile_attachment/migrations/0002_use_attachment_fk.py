import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    """
    Replace direct FileField with reusable Attachment FK (aligned with task_attachments).
    Recreates the join table (demo-safe if old file rows existed).
    """

    dependencies = [
        ("user_profile_attachment", "0001_initial"),
        ("attachments", "0001_initial"),
        ("user_profile", "0002_alter_userprofile_user_one_to_one"),
    ]

    operations = [
        migrations.DeleteModel(name="UserProfileAttachment"),
        migrations.CreateModel(
            name="UserProfileAttachment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "attachment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_profile_attachments",
                        to="attachments.attachment",
                    ),
                ),
                (
                    "user_profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile_attachments",
                        to="user_profile.userprofile",
                    ),
                ),
            ],
        ),
    ]
