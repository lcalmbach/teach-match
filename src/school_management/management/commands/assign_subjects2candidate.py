import traceback
from django.db import transaction
from django.core.management.base import BaseCommand
from datetime import timedelta, date, datetime
from faker import Faker
import pandas as pd
from django.db import connection
from django.conf import settings
import random


from school_management.models import Candidate, Subject
from school_management.helpers import SubstitutionHelper


class Command(BaseCommand):
    help = "Populates the database with fake data"

    def reset_id_sequence(self, model):
        """
        Resets the ID sequence for the specified model.
        This example uses PostgreSQL syntax. Adjust for your database if necessary.
        """
        model.objects.all().delete()

    def handle(self, *args, **kwargs):
        candidates = Candidate.objects.filter(is_candidate=True)
        subjects = list(Subject.objects.all())

        # Define all half-day availability fields
        half_days = [
            "availability_mo_am",
            "availability_mo_pm",
            "availability_tu_am",
            "availability_tu_pm",
            "availability_we_am",
            "availability_we_pm",
            "availability_th_am",
            "availability_th_pm",
            "availability_fr_am",
            "availability_fr_pm",
        ]

        if not subjects:
            self.stdout.write(self.style.ERROR("No subjects available."))
            return

        for candidate in candidates:
            # Randomly assign 1 to 5 subjects
            num_subjects = random.randint(1, 5)
            assigned_subjects = random.sample(subjects, num_subjects)
            candidate.subjects.set(assigned_subjects)

            # Randomly assign availability on 4 to 10 half-days
            num_half_days = random.randint(4, 10)
            selected_half_days = random.sample(half_days, num_half_days)

            # Reset all availability flags first
            for half_day in half_days:
                setattr(candidate, half_day, False)

            # Set the randomly selected half-days to True
            for half_day in selected_half_days:
                setattr(candidate, half_day, True)

            candidate.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f"{candidate.first_name} {candidate.last_name} assigned {num_subjects} subjects and availability on {num_half_days} half-days."
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                "All candidates have been assigned subjects and availability."
            )
        )
