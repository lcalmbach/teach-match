# Generated by Django 5.0.7 on 2024-11-30 06:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("school_management", "0001_initial"),
    ]

    operations = [
        migrations.DeleteModel(
            name="FreeHalfDayType",
        ),
        migrations.CreateModel(
            name="WeekDay",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("school_management.code",),
        ),
        migrations.RemoveField(
            model_name="schoolday",
            name="free_type",
        ),
        migrations.AddField(
            model_name="schoolday",
            name="daypart",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="free_day_type",
                to="school_management.daypart",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="category",
            name="description",
            field=models.TextField(
                blank=True, max_length=255, verbose_name="Beschreibung"
            ),
        ),
        migrations.AlterField(
            model_name="category",
            name="name",
            field=models.CharField(max_length=100, verbose_name="Name"),
        ),
        migrations.AlterField(
            model_name="timeperiod",
            name="day",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="school_management.weekday",
                verbose_name="Wochentag",
            ),
        ),
        migrations.DeleteModel(
            name="DayOfWeek",
        ),
    ]
