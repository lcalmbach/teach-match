# Generated by Django 5.0.7 on 2024-11-07 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("school_management", "0062_person_send_email_person_send_sms"),
    ]

    operations = [
        migrations.AddField(
            model_name="person",
            name="selected_candidate",
            field=models.BooleanField(default=False, verbose_name="Ausgewählt"),
        ),
    ]
