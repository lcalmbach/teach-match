# Generated by Django 5.0.5 on 2024-06-16 08:53

import django.db.models.deletion
from django.db import migrations, models
import django.utils.timezone


def set_default_created_timestamp(apps, schema_editor):
    substitution = apps.get_model('substitution', 'Substitution')
    for obj in substitution.objects.filter(created_timestamp__isnull=True):
        obj.created_timestamp = django.utils.timezone.now()
        obj.save(update_fields=['created_timestamp'])


class Migration(migrations.Migration):

    dependencies = [
        ("school_management", "0017_substitution_minimum_qualification"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="substitution",
            name="end_period",
        ),
        migrations.RemoveField(
            model_name="substitution",
            name="start_period",
        ),
        migrations.AlterField(
            model_name="substitution",
            name="status",
            field=models.ForeignKey(
                default=3,
                on_delete=django.db.models.deletion.SET_DEFAULT,
                related_name="substitution_status",
                to="school_management.substitutionstatus",
                verbose_name="Status Besetzung Vikariat",
            ),
        ),
        migrations.AddField(
            model_name='substitution',
            name='created_timestamp',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.RunPython(set_default_created_timestamp),
    ]

