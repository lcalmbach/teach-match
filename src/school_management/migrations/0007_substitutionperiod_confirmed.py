# Generated by Django 5.0.5 on 2024-05-29 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("school_management", "0006_alter_vacationday_date_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="substitutionperiod",
            name="confirmed",
            field=models.BooleanField(default=False, verbose_name="Bestätigt"),
        ),
    ]
