# Generated by Django 5.0.6 on 2024-07-10 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("jobs", "0005_alter_application_cover_letter"),
    ]

    operations = [
        migrations.AlterField(
            model_name="job",
            name="salary",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]