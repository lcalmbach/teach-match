# Generated by Django 5.0.7 on 2024-11-19 12:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("school_management", "0076_alter_substitutionlesson_candidate"),
    ]

    operations = [
        migrations.AddField(
            model_name="substitution",
            name="durchfuehrung1",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="durchfuehrung1",
                to="school_management.person",
                verbose_name="Durchführung1",
            ),
        ),
        migrations.AddField(
            model_name="substitution",
            name="durchfuehrung2",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="durchfuehrung2",
                to="school_management.person",
                verbose_name="Durchführung2",
            ),
        ),
    ]