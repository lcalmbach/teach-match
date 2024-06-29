# Generated by Django 5.0.5 on 2024-06-22 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("school_management", "0034_delete_availability"),
    ]

    operations = [
        migrations.AddField(
            model_name="substitutioncandidate",
            name="matching_half_days",
            field=models.IntegerField(
                default=0, verbose_name="Übereinstimmende Halbtage"
            ),
        ),
        migrations.AddField(
            model_name="substitutioncandidate",
            name="num_experiences_in_school",
            field=models.IntegerField(
                default=0, verbose_name="Anzahl Erfahrungen in Schule"
            ),
        ),
        migrations.AddField(
            model_name="substitutioncandidate",
            name="num_experiences_with_class",
            field=models.IntegerField(
                default=0, verbose_name="Anzahl Erfahrungen mit Klasse"
            ),
        ),
        migrations.AddField(
            model_name="substitutioncandidate",
            name="num_experiences_with_subjects",
            field=models.IntegerField(
                default=0, verbose_name="Anzahl Erfahrungen mit Fach"
            ),
        ),
    ]