# Generated by Django 4.2.1 on 2023-05-28 15:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("sonet", "0008_rename_hashtags_post_hashtag"),
    ]

    operations = [
        migrations.AlterField(
            model_name="hashtag",
            name="name",
            field=models.CharField(max_length=50),
        ),
    ]