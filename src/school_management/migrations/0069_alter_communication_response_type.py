# Generated by Django 5.0.7 on 2024-11-12 05:55

import django.db.models.deletion
import school_management.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("school_management", "0068_communication_comment_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="communication",
            name="response_type",
            field=models.ForeignKey(
                blank=True,
                default=school_management.models.default_communication_response_type,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="communication_response_type",
                to="school_management.communicationresponsetype",
            ),
        ),
    ]
