# Generated by Django 4.2.1 on 2023-06-02 11:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("sonet", "0014_alter_post_comment"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="post",
            name="comment",
        ),
        migrations.RemoveField(
            model_name="post",
            name="likes",
        ),
        migrations.AlterField(
            model_name="like",
            name="post",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="likes",
                to="sonet.post",
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]