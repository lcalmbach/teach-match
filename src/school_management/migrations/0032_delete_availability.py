# Generated by Django 5.0.5 on 2024-06-22 10:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("school_management", "0031_rename_short_name_dayofweek_name_short_and_more"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Availability",
        ),
    ]
