# Generated by Django 4.2.6 on 2024-11-21 02:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("articles", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="commit",
            old_name="commit",
            new_name="content",
        ),
    ]
