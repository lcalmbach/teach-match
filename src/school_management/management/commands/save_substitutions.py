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

today = datetime.now()
end_of_year = datetime(today.year, 12, 31)
all_days, all_periods = [],[]
        

def generate_date_list(year):
    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 31)

    # Generate a list of all dates in the year 2024
    date_list = []
    current_date = start_date
    while current_date <= end_date:
        if current_date.weekday() < 5:
            date_list.append(current_date)
        current_date += timedelta(days=1)
    return date_list


class Command(BaseCommand):
    help = "Populates the database with fake data"

    def reset_id_sequence(self, model):
        """
        Resets the ID sequence for the specified model.
        This example uses PostgreSQL syntax. Adjust for your database if necessary.
        """
        model.objects.all().delete()

    def add_substitutions(self, faker):
        print("Creating substitutions...")
        
        try:
            for s in Substitution.objects.all():
                helper = SubstitutionHelper(s)
                s = helper.assign_values()
                s.save()
            print("Substitutions created.")
        except Exception as e:
            print(e)
            return False
        return True

    def handle(self, *args, **kwargs):
        global all_days
        global all_periods
        faker = Faker("de_DE")
        
        for subtitution in Substitution.objects.all():
            subtitution.save()

