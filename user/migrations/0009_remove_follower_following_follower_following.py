# Generated by Django 4.2.1 on 2023-05-31 19:51

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0008_alter_follower_following"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="follower",
            name="following",
        ),
        migrations.AddField(
            model_name="follower",
            name="following",
            field=models.ManyToManyField(
                related_name="user_following",
                to=settings.AUTH_USER_MODEL,
                verbose_name="follower",
            ),
        ),
    ]
