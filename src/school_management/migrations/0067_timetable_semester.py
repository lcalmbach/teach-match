# Generated by Django 5.0.7 on 2024-11-09 07:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("school_management", "0066_semester_alter_person_send_email_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="timetable",
            name="semester",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="timetable_semesters",
                to="school_management.semester",
            ),
            preserve_default=False,
        ),
    ]