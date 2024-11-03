import traceback
from django.db import transaction
from django.core.management.base import BaseCommand
from datetime import timedelta, date, datetime
from faker import Faker
import pandas as pd
from django.db import connection
from django.conf import settings


from school_management.models import (
    Substitution,
)
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
        for substitution in Substitution.objects.all():
            helper = SubstitutionHelper(substitution)
            substitution = helper.assign_values()
            print(substitution)
            substitution.save()