# Generated by Django 4.2.6 on 2024-11-25 03:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("articles", "0003_alter_article_user"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Commitlike",
        ),
    ]
