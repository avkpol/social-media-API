# Generated by Django 4.2.1 on 2023-05-30 17:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0004_remove_userprofile_id_alter_userprofile_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="bio",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="user",
            name="profile_picture",
            field=models.ImageField(
                blank=True, null=True, upload_to="profile_pictures/"
            ),
        ),
        migrations.DeleteModel(
            name="UserProfile",
        ),
    ]