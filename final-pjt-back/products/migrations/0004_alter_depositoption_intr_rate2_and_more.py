# Generated by Django 4.2.6 on 2024-11-25 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0003_alter_depositoption_deposit_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="depositoption",
            name="intr_rate2",
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name="depositoption",
            name="intr_type",
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name="depositoption",
            name="intr_type_name",
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name="savingoption",
            name="intr_rate2",
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name="savingoption",
            name="intr_type",
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name="savingoption",
            name="intr_type_name",
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name="savingoption",
            name="rsrv_type",
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name="savingoption",
            name="rsrv_type_name",
            field=models.CharField(max_length=250, null=True),
        ),
    ]
