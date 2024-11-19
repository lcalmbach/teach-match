import random
from django.core.management.base import BaseCommand
from datetime import timedelta, date, datetime
from faker import Faker



from school_management.models import (
    Candidate,
    Subject
)


today = datetime.now()
end_of_year = datetime(today.year, 12, 31)
all_days, all_periods = [], []


class Command(BaseCommand):
    help = "Populates the database with fake data"

    def fill_availability_candidates(self):
        for candidate in Candidate.objects.all():     
            half_days_no = random.randint(2, 10)
            half_days_list = ['mo_am', 'mo_pm','tu_am','tu_pm','we_am','we_pm','th_am','th_pm','fr_am','fr_pm']
            for key in half_days_list:
                setattr(candidate, 'availability_' + key, False)
            half_days_list = random.sample(half_days_list, half_days_no)
            for key in half_days_list:
                setattr(candidate, 'availability_' + key, True)
                candidate.save()

    def fill_subjects(self):
        subjects = Subject.objects.all()
        subjets_no = len(subjects)
        for candidate in Candidate.objects.all():
            subjects_no = random.randint(3, subjets_no)
            subjects_list = random.sample(list(subjects), subjects_no)
            candidate.subjects.set(subjects_list)
            candidate.save()


    def handle(self, *args, **kwargs):
        # self.fill_availability_candidates()
        # self.fill_subjects()
    


    