# Generated by Django 5.0.5 on 2024-06-21 05:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("school_management", "0026_remove_subject_school_year"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="subject",
            name="course",
        ),
    ]