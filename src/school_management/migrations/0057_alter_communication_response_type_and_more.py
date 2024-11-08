# Generated by Django 5.0.7 on 2024-08-21 04:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("school_management", "0056_substitutioncandidate_selected_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="communication",
            name="response_type",
            field=models.ForeignKey(
                default=4,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="communication_response_type",
                to="school_management.communicationresponsetype",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="person",
            name="available_to_date",
            field=models.DateField(blank=True, null=True, verbose_name="Verfügbar bis"),
        ),
    ]
