# Generated by Django 4.2.8 on 2023-12-24 16:27

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("mainapp", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Employer",
            fields=[
                (
                    "customuser_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="mainapp.customuser",
                    ),
                ),
                ("company_name", models.CharField(max_length=255)),
                ("industry", models.CharField(max_length=100)),
                ("founded_date", models.DateField(blank=True, null=True)),
                ("description", models.TextField(blank=True, null=True)),
                ("mission_statement", models.TextField(blank=True, null=True)),
                (
                    "company_logo",
                    models.ImageField(
                        blank=True, null=True, upload_to="employer_logos/"
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            bases=("mainapp.customuser",),
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Job",
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
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("requirements", models.TextField()),
                ("location", models.CharField(max_length=255)),
                ("salary", models.DecimalField(decimal_places=2, max_digits=10)),
                ("published_date", models.DateField(auto_now_add=True)),
                ("deadline", models.DateField()),
                ("is_active", models.BooleanField(default=True)),
                (
                    "employer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="related_jobs",
                        to="employer.employer",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="employer",
            name="posted_jobs",
            field=models.ManyToManyField(
                blank=True, related_name="related_employers", to="employer.job"
            ),
        ),
    ]
