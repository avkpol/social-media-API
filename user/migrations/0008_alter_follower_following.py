# Generated by Django 4.2.1 on 2023-05-31 19:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0007_remove_follower_follower_alter_follower_following_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="follower",
            name="following",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_following",
                to=settings.AUTH_USER_MODEL,
                verbose_name="follower",
            ),
        ),
    ]
