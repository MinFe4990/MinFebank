# Generated by Django 4.2.6 on 2024-11-19 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="saving",
            name="special_cnd",
            field=models.CharField(max_length=255),
        ),
    ]