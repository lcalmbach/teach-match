# Generated by Django 5.0.7 on 2024-08-19 04:57

import django.db.models.deletion
import school_management.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "school_management",
            "0055_rename_communicationanswertype_communicationresponsetype_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="substitutioncandidate",
            name="selected",
            field=models.BooleanField(default=False, verbose_name="Ausgewählt"),
        ),
        migrations.AlterField(
            model_name="substitution",
            name="cause",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="substitution_causes",
                to="school_management.substitutioncause",
                verbose_name="Begründung",
            ),
        ),
        migrations.AlterField(
            model_name="substitution",
            name="status",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.SET_DEFAULT,
                related_name="substitution_status",
                to="school_management.substitutionstatus",
                verbose_name="Status Besetzung Vikariat",
            ),
        ),
    ]