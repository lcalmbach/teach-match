# Generated by Django 5.0.7 on 2024-08-23 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("school_management", "0059_person_gender"),
    ]

    operations = [
        migrations.AddField(
            model_name="substitutioncandidate",
            name="matching_subjects",
            field=models.IntegerField(
                default=0, verbose_name="Übereinstimmende Fächer"
            ),
        ),
    ]
