# Generated by Django 3.1.4 on 2022-12-02 17:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="updated_at",
        ),
    ]
