# Generated by Django 5.0.7 on 2024-11-30 10:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("school_management", "0006_school_code"),
    ]

    operations = [
        migrations.RenameField(
            model_name="person",
            old_name="phone_number",
            new_name="mobile",
        ),
    ]