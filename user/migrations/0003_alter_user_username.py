# Generated by Django 4.2.1 on 2023-05-29 16:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0002_follower_userprofile_alter_user_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(
                blank=True,
                max_length=150,
                null=True,
                unique=True,
                verbose_name="username",
            ),
        ),
    ]
