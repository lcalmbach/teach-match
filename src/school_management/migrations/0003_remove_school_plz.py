# Generated by Django 5.0.7 on 2024-11-30 06:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("school_management", "0002_delete_freehalfdaytype_weekday_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="school",
            name="plz",
        ),
    ]
