# Generated by Django 5.0.7 on 2024-08-05 05:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "school_management",
            "0054_alter_communicationanswertype_options_person_gender",
        ),
    ]

    operations = [
        migrations.RenameModel(
            old_name="CommunicationAnswerType",
            new_name="CommunicationResponseType",
        ),
        migrations.RenameField(
            model_name="communication",
            old_name="answer_date",
            new_name="response_date",
        ),
        migrations.RenameField(
            model_name="communication",
            old_name="answer_text",
            new_name="response_text",
        ),
        migrations.RemoveField(
            model_name="communication",
            name="answer_type",
        ),
        migrations.AddField(
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
