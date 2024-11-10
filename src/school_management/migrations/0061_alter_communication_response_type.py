# Generated by Django 5.0.7 on 2024-11-04 05:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("school_management", "0060_substitutioncandidate_matching_subjects"),
    ]

    operations = [
        migrations.AlterField(
            model_name="communication",
            name="response_type",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="communication_response_type",
                to="school_management.communicationresponsetype",
            ),
        ),
    ]
