# Generated by Django 4.2.1 on 2023-05-28 14:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("sonet", "0006_post_comments_post_likes_remove_post_hashtags_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="post",
            name="hashtags",
        ),
        migrations.AddField(
            model_name="post",
            name="hashtags",
            field=models.ManyToManyField(
                blank=True, related_name="posts", to="sonet.hashtag"
            ),
        ),
    ]
