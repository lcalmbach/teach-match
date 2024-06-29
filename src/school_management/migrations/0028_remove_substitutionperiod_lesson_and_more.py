# Generated by Django 5.0.5 on 2024-06-21 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("school_management", "0027_remove_subject_course"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="substitutionperiod",
            name="lesson",
        ),
        migrations.RemoveField(
            model_name="substitutionperiod",
            name="deputy",
        ),
        migrations.RemoveField(
            model_name="substitutionperiod",
            name="substitution",
        ),
        migrations.AddField(
            model_name="subject",
            name="short_name",
            field=models.CharField(blank=True, max_length=255, verbose_name="Kürzel"),
        ),
        migrations.DeleteModel(
            name="Lesson",
        ),
        migrations.DeleteModel(
            name="SubstitutionPeriod",
        ),
    ]