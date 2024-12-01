import traceback
from django.db import transaction
from django.core.management.base import BaseCommand
from datetime import timedelta, date, datetime
from faker import Faker
import pandas as pd
from school_management.models import (
    School,
    Level,
    Location,
    Certificate,
    Person,
    Candidate,
    Teacher,
    Substitution,
    Qualification,
    Subject,
    WeekDay,
    TimePeriod,
    DayPart,
    Gender,
    SchoolPersonRole,
    SchoolClass,
    SubstitutionCause,
    SubstitutionStatus,
    SubstitutionCandidate,
    CommunicationType,
    CommunicationResponseType,
    Timetable,
    CodeEnum,
    Code,
    Category,
)
from django.db import connection
import random
import os
import shutil
import fitz  # PyMuPDF
from django.conf import settings
from django.contrib.auth.models import User, Group

today = datetime.now()
end_of_year = datetime(today.year, 12, 31)
all_days, all_periods = [], []


class Command(BaseCommand):
    help = "Populates the database with fake data"

    def reset_id_sequence(self, model):
        """
        Resets the ID sequence for the specified model.
        This example uses PostgreSQL syntax. Adjust for your database if necessary.
        """
        model.objects.all().delete()

    
    def fill_categories(self):
        filename = "./data/code_category.csv"
        try:
            df = pd.read_csv(filename, sep=";")
            for index, row in df.iterrows():
                data = {"id": row["id"], "name": row["name"], "description": row["description"]}
                Category.objects.create(**data)  
            print(f"Codes for {filename} created.")
            return True
        except Exception as e:
            print(e)
            return False

    def fill_codes(self, codes: list):
        filename = "./data/codes.csv"
        try:
            df = pd.read_csv(filename, sep=";")
            for code in codes:
                Location.objects.filter(category_id=code).delete()
                for index, row in df.iterrows():
                    data = {"category_id": row["category_id"], "name": row["name"], "description": row["description"], "short_name": row["short_name"]}
                    if row["category_id"] == code:
                        data = {
                            "category": Category.objects.get(pk=row["category_id"]),
                            "name": row["name"], 
                            "description": row["description"],
                            "order": row["order"],
                            "short_name": row["short_name"],
                        }
                        Code.objects.create(**data)
                print(f"codes for {code} created.")
        except Exception as e:
            print(e)
            return False
            return True

    
    def fill_timeperiods(self):
        print("filling time periods")
        try:
            TimePeriod.objects.all().delete()
            df = pd.read_csv("./data/timeperiods.csv", sep=";")
            for index, row in df.iterrows():
                TimePeriod.objects.create(
                    code=row["id"],
                    day = WeekDay.objects.get(order=row["day"]),
                    start_time=row["start"],
                    end_time=row["end"],
                )
            print("time periods created.")
            return True
        except Exception as e:
            print(e)
            return False
        
    def fill_levels(self):
        print("filling levels")
        try:
            Level.objects.all().delete()
            df = pd.read_csv("./data/levels.csv", sep=";")
            for index, row in df.iterrows():
                Level.objects.create(
                    id=row["id"],
                    name=row["name"],
                )
            print("time levels.")
            return True
        except Exception as e:
            print(e)
            return False
        
    def fill_teachers(self):
        print("filling teachers")
        try:
            Teacher.objects.all().delete()
            filename = "./data/teachers.csv"
            df = pd.read_csv(filename, sep=";")
            for index, row in df.iterrows():
                last_name = row["name"].split(" ")[0]
                first_name = row["name"].split(" ")[1]
                usr = User.objects.get(username=row["id"])
                if not usr:
                    usr = User.objects.create_user(username=row["id"], password="pasword", first_name=first_name, last_name=last_name)
                Teacher.objects.create(
                    user=usr,
                    first_name=first_name,
                    last_name=last_name,
                    initials = row["id"],
                    email='lcalmbach@gmail.com',
                    mobile='+41791742159',
                    is_teacher=True,
                    gender=Gender.objects.get(short_name='f') if first_name[-1] == 'a' else Gender.objects.get(short_name='m'),
                )
        except Exception as e:
            print(traceback.format_exc())  # This prints the whole traceback
            print(e)
            return False
        print("codes for schools created.")
        return True


    def fill_school(self):
        print("filling time periods")

        try:
            School.objects.all().delete()
            filename = "./data/school.csv"
            df = pd.read_csv(filename, sep=";")
            for index, row in df.iterrows():
                School.objects.create(
                    id=row["id"],
                    name=row["name"],
                    address=row["address"],
                    url=row["url"],
                    level=Level.objects.get(name_short=row["level"]),
                    location=Location.objects.get(short_name=row["plz"]),
                    email=row["email"],
                    phone_number=row["phone"],
                    mobile=row["mobile"],
                    code=row["code"],
                )
        except Exception as e:

            print(traceback.format_exc())  # This prints the whole traceback
            print(e)
            return False
        print("codes for schools created.")
        return True


    def fill_timetable(self, force: bool = False):
        """Create timetable template for each school and teacher"""

        try:
            if force:
                Timetable.objects.all().delete()

            timetable_df = pd.read_csv("./data/timetable.csv", sep=";")
            for index, row in timetable_df.iterrows():                    
                teacher = Teacher.objects.filter(initials=row["id"])[
                    0
                ]  # Assuming 'initials' uniquely identifies a Teacher
                print(teacher.initials)
                school_class = SchoolClass.objects.filter(
                    name=row["school_class_name"], school_id=row["school_id"]
                )[
                    0
                ]  # Assuming this combination uniquely identifies a SchoolClass
                print(
                    row["subject_name_short"],
                    len(Subject.objects.filter(name_short=row["subject_name_short"])),
                )
                subject = Subject.objects.filter(name_short=row["subject_name_short"])[
                    0
                ]  # Assuming 'id' uniquely identifies a Subject
                print(row["subject_name_short"])
                Timetable.objects.create(
                    teacher=teacher,
                    school_id=row["school_id"],
                    day_id=row["weekday_number"],
                    period_id=row["lektion_number"],
                    school_class=school_class,
                    subject=subject,
                )
            print(f"Timetable template created.")
        except Exception as e:
            print(e)
            return False
        return True

    

    def handle(self, *args, **kwargs):
        global all_days
        global all_periods
        faker = Faker("de_DE")
        ok = True
        """if ok:
            ok = self.fill_categories()
        
        if ok:
            ok = self.fill_codes([9])
        
        ok = self.fill_timeperiods()
        if not ok:
            print("An error occurred while populating the data.")
        
        if ok:
            ok = self.fill_levels()        
        if ok:
            ok = self.fill_school()
        if ok:
            ok = self.fill_timeperiods()
        """
        if ok:
            ok = self.fill_teachers()
        if not ok:
            print("An error occurred while populating the data.")    