# Generated by Django 4.2.6 on 2024-11-19 05:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Bank",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("code", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Deposit",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=250)),
                ("code", models.CharField(max_length=250)),
                ("join_way", models.CharField(max_length=250)),
                ("final_init", models.CharField(max_length=250)),
                ("special_cnd", models.CharField(max_length=250)),
                ("start_day", models.DateField()),
                ("end_day", models.DateField(null=True)),
                ("max_limit", models.IntegerField(null=True)),
                ("join_member", models.CharField(max_length=250)),
                (
                    "bank",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="products.bank"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DepositOption",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("intr_type", models.CharField(max_length=250)),
                ("intr_type_name", models.CharField(max_length=250)),
                ("save_term", models.IntegerField()),
                ("intr_rate", models.FloatField(null=True)),
                ("intr_rate2", models.FloatField()),
                (
                    "deposit",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="products.deposit",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="JoinDeny",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("join_deny", models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name="Saving",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=250)),
                ("code", models.CharField(max_length=250)),
                ("join_way", models.CharField(max_length=250)),
                ("final_init", models.CharField(max_length=250)),
                ("special_cnd", models.CharField(max_length=250)),
                ("start_day", models.DateField()),
                ("end_day", models.DateField(null=True)),
                ("max_limit", models.IntegerField(null=True)),
                ("join_member", models.CharField(max_length=250)),
                (
                    "bank",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="products.bank"
                    ),
                ),
                (
                    "join_deny",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="products.joindeny",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SavingOption",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("intr_type", models.CharField(max_length=250)),
                ("intr_type_name", models.CharField(max_length=250)),
                ("save_term", models.IntegerField()),
                ("intr_rate", models.FloatField(null=True)),
                ("intr_rate2", models.FloatField()),
                ("rsrv_type", models.CharField(max_length=250)),
                ("rsrv_type_name", models.CharField(max_length=250)),
                (
                    "saving",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="products.saving",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SignedDeposit",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "deposit",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="products.deposit",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SignedSaving",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "saving",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="products.saving",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SignedSavingOption",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "saving_option",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="products.savingoption",
                    ),
                ),
                (
                    "signed_saving",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="products.signedsaving",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SignedDepositOption",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "deposit_option",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="products.depositoption",
                    ),
                ),
                (
                    "signed_deposit",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="products.signeddeposit",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="deposit",
            name="join_deny",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="products.joindeny"
            ),
        ),
    ]