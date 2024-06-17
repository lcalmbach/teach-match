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
    PersonCertificate,
    PersonSubject,
    Substitution,
    SubstitutionPeriod,
    Qualification,
    Subject,
    DayOfWeek,
    Course,
    Period,
    TimeOfDay,
    Gender,
    SchoolPersonRole,
    SchoolPerson,
    SchoolClass,
    LessonTemplate,
    AvailabilityTemplate,
    Availability,
    SubstitutionCause,
    Lesson,
    VacationTemplate,
    SubstitutionStatus,
    SubstitutionCandidate
)
from django.db import connection
import random
import os
import shutil
import fitz  # PyMuPDF
from django.conf import settings

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


def get_random_teacher(school_id):
    # Filter SchoolPerson based on role and school, and order results randomly
    role = SchoolPersonRole.objects.get(id=4)
    teachers = SchoolPerson.objects.filter(role=role, school_id=school_id)
    if teachers.exists():
        return random.choice(list(teachers)).person
    else:
        return None
            
def extract_text_from_pdf(pdf_path):
    # Open the PDF file
    with fitz.open(pdf_path) as doc:
        text = ""
        for page in doc:
            text += page.get_text()
    return text


class Command(BaseCommand):
    help = "Populates the database with fake data"

    def reset_id_sequence(self, model):
        """
        Resets the ID sequence for the specified model.
        This example uses PostgreSQL syntax. Adjust for your database if necessary.
        """
        model.objects.all().delete()


    def fill_teachers_candidates(self, faker, force=True):
        try:
            if force:
                Person.objects.filter().delete()
            # teachers
            num_entries = 50
            for _ in range(num_entries):
                Person.objects.create(
                    first_name=faker.first_name(),
                    last_name=faker.last_name(),
                    email='lukas.calmbach@bs.com',
                    phone_number='+41791742159',
                    gender=random.choice(Gender.objects.all()),
                    year_of_birth=faker.random_int(min=1990, max=2004),
                    cv_text=faker.text(max_nb_chars=200),

                    is_teacher=True,
                    is_candidate=random.choice([True, False]),
                    years_of_experience=faker.random_int(min=1, max=30),
                )
            print("Teachers created...")

            # deputy candidates
            num_entries = 100
            for _ in range(num_entries):
                Person.objects.create(
                    first_name=faker.first_name(),
                    last_name=faker.last_name(),
                    email='lukas.calmbach@bs.com',
                    phone_number='+41791742159',
                    gender=random.choice(Gender.objects.all()),
                    year_of_birth=faker.random_int(min=1990, max=2004),
                    cv_text=faker.text(max_nb_chars=200),
                    is_teacher=False,
                    is_candidate=True,
                    years_of_experience=faker.random_int(min=0, max=30),
                )
            print("Candidates created...")
        except Exception as e:
            print(e)
            return False
        return True

    def fill_school_contacts(self, faker, force=True):
        try:
            if force:
                SchoolPerson.objects.filter().delete()

            for school in School.objects.all():
                rector = Person.objects.create(
                    first_name=faker.first_name(),
                    last_name=faker.last_name(),
                    email='lukas.calmbach@bs.com',
                    phone_number='+41791742159',
                    gender=random.choice(Gender.objects.all()),
                    year_of_birth=faker.random_int(min=1990, max=2004),
                    cv_text=faker.text(max_nb_chars=200),
                    is_teacher=False,
                    is_candidate=False,
                    is_leitung=True,
                    years_of_experience=faker.random_int(min=1, max=30),
                )
                SchoolPerson.objects.create(
                    school=school,
                    person=rector,
                    role=SchoolPersonRole.objects.get(id=1),
                    description="Leitung"
                )
                print(f"School contact for {school.name} created...")

            print("School contacts created...")

            # deputy candidates
            num_entries = 100
            for _ in range(num_entries):
                Person.objects.create(
                    first_name=faker.first_name(),
                    last_name=faker.last_name(),
                    email='lukas.calmbach@bs.com',
                    phone_number='+41791742159',
                    gender=random.choice(Gender.objects.all()),
                    year_of_birth=faker.random_int(min=1990, max=2004),
                    cv_text=faker.text(max_nb_chars=200),
                    is_teacher=False,
                    is_candidate=True,
                    years_of_experience=faker.random_int(min=0, max=30),
                )
        except Exception as e:
            print(e)
            return False
        print("candidates created...")
        return True
    

    def fill_deputies(self, faker, force=True):
        print("Creating teachers...")
        try:
            if force:
                Person.objects.filter(is_candidate=True).delete()
            
            num_entries = 50
            for _ in range(num_entries):
                Person.objects.create(
                    first_name=faker.first_name(),
                    last_name=faker.last_name(),
                    email='lukas.calmbach@bs.com',
                    phone_number='+41791742159',
                    gender=random.choice(Gender.objects.all()),
                    year_of_birth=faker.random_int(min=1990, max=2004),
                    cv_text=faker.text(max_nb_chars=200),
                    is_teacher=random.choice([True, False]),
                    
                    years_of_experience=faker.random_int(min=0, max=30),
                )
        except Exception as e:
            print(e)
            return False
        print("teachers created.")
        return True


    def add_person_certificate(self, faker):
        print("Creating candidate certificate...")
        self.reset_id_sequence(PersonCertificate)
        persons = list(Person.objects.all())
        certificates = list(Certificate.objects.all())

        try:
            for person in persons:
                year = faker.random_int(min=1983, max=2004)
                PersonCertificate.objects.create(
                    person=person, certificate=random.choice(certificates), year=year
                )
                PersonCertificate.objects.create(
                    person=person,
                    certificate=random.choice(certificates),
                    year=year + 1,
                )
            print("Certificates created and assigned.")
        except Exception as e:
            print(e)
            return False
        return True

    def assign_cvs_to_candidates(self):
        source_filenames = [f"{settings.MEDIA_ROOT}\cv\{x+1}.pdf" for x in range(6)]
        try:
            for candidate in Person.objects.all():
                source_filename = random.choice(source_filenames)
                target_filename = f"{settings.MEDIA_ROOT}\cv\{candidate.pk}.pdf"

                # Ensure the 'cv' directory exists
                os.makedirs(os.path.dirname(target_filename), exist_ok=True)

                # Copy the file
                shutil.copy(source_filename, target_filename)

                # Extract text from the copied PDF
                text = extract_text_from_pdf(target_filename)

                # Assign extracted text and filename to the candidate
                candidate.cv_text = text
                candidate.cv_file = f"\cv\{candidate.pk}.pdf"
                candidate.save()
            print("CVs assigned.")
        except Exception as e:
            print(e)
            return False
        return True


    def add_substitutions(self, faker):
        print("Creating substitutions...")
        self.reset_id_sequence(Substitution)
        teacher_ids = Person.objects.filter(is_teacher=True).values_list('id', flat=True)
        teacher_ids = list(teacher_ids)
        random.shuffle(teacher_ids)
        selected_teacher_ids = teacher_ids[:20]
        selected_teachers = Person.objects.filter(id__in=selected_teacher_ids)
        all_causes = list(SubstitutionCause.objects.all())
        try:
            for teacher in selected_teachers:
                start_date = today + timedelta(days=random.randint(1, (end_of_year - today).days))
                end_date = start_date + timedelta(days=random.randint(1, 30))
                Substitution.objects.create(
                    teacher=teacher,
                    start_date=start_date,
                    end_date=end_date,
                    start_period=Period.objects.get(pk=3),
                    end_period=Period.objects.get(pk=3),
                    cause = random.choice(all_causes),
                )
            print("Substitutions created.")
        except Exception as e:
            print(e)
            return False
        return True

    def fill_dayofweek(force: bool = False):
        try:
            if force:
                DayOfWeek.objects.all().delete()
            df = pd.read_csv('./data/dayofweek.csv', sep=';')
            for index, row in df.iterrows():
                DayOfWeek.objects.create(
                    id=row['id'],
                    name=row['name'],
                    short_name=row['short_name']
                )
        except Exception as e:
            print(e)
            return False
        print("codes for DayOfWeek created.")
        return True


    def fill_subjects(self, force: bool=True):
        try:
            if force:
                Subject.objects.all().delete()
            filename = './data/subjects.csv'
            df = pd.read_csv(filename, sep=';')
            for index, row in df.iterrows():
                Subject.objects.create(
                    id=row['id'],
                    name=row['name'],
                    description=row['description'],
                    course_id=row['course_id'],
                    school_year=row['school_year'],
                )
            print(f"codes for {filename} created.")
        except Exception as e:
            print(e)
            return False
        return True
    

    def fill_code(self, model, filename, force: bool=True):
        try:
            if force:
                model.objects.all().delete()
            df = pd.read_csv(filename, sep=';')
            for index, row in df.iterrows():
                data = {
                    'id': row['id'],
                    'name': row['name']
                }
                if 'description' in [field.name for field in model._meta.get_fields()]:
                    data['description'] = row['description']
                model.objects.create(**data)
            print(f"codes for {filename} created.")
        except Exception as e:
            print(e)
            return False
        return True


    def fill_period(self, force: bool = False):
        try:
            if force:
                Period.objects.all().delete()
            df = pd.read_csv('./data/period.csv', sep=';')
            for index, row in df.iterrows():
                Period.objects.create(
                    id=row['id'], 
                    start_time=row['start_time'], 
                    end_time=row['end_time'], 
                    time_of_day=random.choice(list(TimeOfDay.objects.all())),
                )
        except Exception as e:
            print(e)
            return False
        print("codes for courses created.")
        return True
    
    def fill_school(self, force: bool=False):
        # id; name;address;url;plz;level_id;location_id
        try:
            if force:
                School.objects.all().delete()
            df = pd.read_csv('./data/school.csv', sep=';')
            for index, row in df.iterrows():
                School.objects.create(
                    id=row['id'],
                    name=row['name'],
                    address=row['address'],
                    plz=row['plz'],
                    url=row['url'],
                    level=Level.objects.get(id=row['level_id']),
                    location=Location.objects.get(id=row['location_id']),
                )
        except Exception as e:
            
            print(traceback.format_exc())  # This prints the whole traceback
            print(e)
            return False
        print("codes for schools created.")
        return True

    def assign_teachers_to_schools(self, force: bool=False):
        # id; name;address;url;plz;level_id;location_id
        try:
            if force:
                pass
            for person in Person.objects.filter(is_teacher=True):
                school = random.choice(School.objects.all())
                SchoolPerson.objects.create(
                    school=school,
                    person=person,
                    role=SchoolPersonRole.objects.get(id=4),
                    description="Lehrperson"
                )
        except Exception as e:
            print(traceback.format_exc())  # This prints the whole traceback
            print(e)
            return False
        print("teachers have been assigned to schools.")
        return True
    

    def fill_timetable_template(self, force: bool=False):
        """Create timetable template for each school and teacher"""
        try:
            if force:
                LessonTemplate.objects.all().delete()
            
            for teacher in Person.objects.filter(is_teacher=True):
                school = teacher.school_persons.first().school
                for day in random.sample(all_days, 3):
                    for period in random.sample(all_periods, 5):
                        subject = random.choice(Subject.objects.all())
                        LessonTemplate.objects.create(
                            teacher=teacher,
                            school=school,
                            day=day,
                            period=period,
                            school_class=random.choice(SchoolClass.objects.filter(school=school)),
                            frequency=1,
                            subject=subject,
                        )
            print(f"Timetable template created.")
        except Exception as e:
            print(e)
            return False
        return True

    
    def fill_classes(self, force: bool=False):
        try:
            if force:
                SchoolClass().objects.all().delete()
            filename = './data/schoolclass.csv'
            df = pd.read_csv(filename, sep=';')
            for index, row in df.iterrows():
                teacher = get_random_teacher(row['school'])
                school = School.objects.get(id=row['school'])
                SchoolClass.objects.create(
                    name=row['name'],
                    school=school,
                    contact_person=teacher,
                    level=Level.objects.get(id=row['level']),
                    school_year=row['school_year'],
                )
            print(f"classes created.")
        except Exception as e:
            print(e)
            return False
        return True

    def fill_person_subject(self, force: bool=False):
        try:
            if force:
                PersonSubject.objects.all().delete()
            for person in Person.objects.filter():
                no_of_subjects = random.randint(1, 4)
                for _ in range(1, no_of_subjects):
                    subject = random.choice(Subject.objects.all())
                    a = PersonSubject.objects.create(
                        person=person,
                        subject=subject,
                        experience=random.randint(1, 5),
                    )
            print("Subjects have been assigned to teachers.")
        except Exception as e:
            print(e)
            return False
        return True
    
    def fill_availabilities(self, force: bool=False):
        day_ids = DayOfWeek.objects.values_list('id', flat=True)
        try:
            if force:
                AvailabilityTemplate.objects.all().delete()
            for candidate in Candidate.objects.all():
                from_date = today + timedelta(days=random.randint(1, (end_of_year - today).days))
                weeks_range = random.randint(1, 10)
                AvailabilityTemplate.objects.create(
                    candidate=candidate,
                    date_from = from_date,
                    date_to = from_date + + timedelta(weeks=weeks_range),
                    day_of_week = DayOfWeek.objects.get(id=8),
                    time_of_day = TimeOfDay.objects.get(id=3)
                )
            print("availabilities have been assigned")
        except Exception as e:
            print(e)
            return False
        return True
        

    def fill_timetable(self, force: bool=False):
        try:
            if force:
                Lesson.objects.all().delete()
            days_in_year = generate_date_list(2024)

            for date in days_in_year:
                day_id = date.weekday() + 1
                for lesson_template in LessonTemplate.objects.filter(day=DayOfWeek.objects.get(id=day_id)):
                    Lesson.objects.create(
                        teacher=lesson_template.teacher,
                        date=date,
                        school=lesson_template.school,
                        period=lesson_template.period,
                        school_class=lesson_template.school_class,
                        subject=lesson_template.subject,
                    )

        except Exception as e:
            print(e)
            return False
        print("Lessons have been assigned to teachers.")
        return True
    
    def fill_vacation(self, force: bool=False):
        try:
            if force:
                VacationTemplate.objects.all().delete()
            filename = './data/vacation.csv'
            df = pd.read_csv(filename, sep=';')
            with transaction.atomic():
                for index, row in df.iterrows():
                    VacationTemplate.objects.create(
                        name = row['name'],
                        date_from = row['date_from'],
                        date_to = row['date_to'],
                        timeofday = TimeOfDay.objects.get(pk=row['time_of_day']),
                    )
            print(VacationTemplate.objects.all())
            print(f"vacation created.")
        except Exception as e:
            print(e)
            return False
        return True
    
    def fill_substitution_candidates(self, force: bool=False):
        """
        Fill substitution candidates.
        """
        try:
            if force:
                SubstitutionCandidate.objects.all().delete()
            for substitution in Substitution.objects.all():
                for _ in range(random.randint(1, 10)):
                    candidate = random.choice(Candidate.objects.all())
                    SubstitutionCandidate.objects.create(
                        substitution=substitution,
                        candidate=candidate,
                        rating=random.randint(1, 100)
                    )
            print("substitution candidates created.")
        except Exception as e:
            print(e)
            return False
        return True

    def handle(self, *args, **kwargs):
        global all_days
        global all_periods
        faker = Faker("de_DE")
        ok = True
        
        force_reset = True
        if ok:
            ok = self.fill_code(Qualification, './data/qualification.csv', force_reset)
        ok = False
        if ok:
            ok = self.fill_code(SubstitutionStatus, './data/substitutionstatus.csv', force_reset)
        if ok:
            ok = self.school_year('./data/schoolyear.csv', force_reset)
        if ok:
            ok = self.fill_vacation(force_reset)
        if ok:
            ok = self.fill_code(SubstitutionCause, './data/substitutioncause.csv', force_reset)
        if ok:
            ok = self.fill_code(Course, './data/course.csv', force_reset)
        if ok:
            ok = self.fill_code(Gender,'./data/gender.csv', force_reset)
        if ok:
            ok = self.fill_code(SchoolPersonRole, './data/schoolpersonrole.csv', force_reset)
        if ok:
            ok = self.fill_code(TimeOfDay,'./data/timeofday.csv', force_reset)
        if ok:
            ok = self.fill_dayofweek()
        if ok:
            ok = self.fill_code(Level,'./data/level.csv', force_reset)
        if ok:
            ok = self.fill_code(Certificate,'./data/certificate.csv', force_reset)
        if ok:
            ok = self.fill_code(Location,'./data/location.csv', force_reset)
        
        all_days = list(DayOfWeek.objects.all())
        all_periods = list(Period.objects.all())

        # tables with dependencies
        if ok:
            ok = self.fill_subjects()
        if ok:
            ok = self.fill_period(faker)
        if ok:
            ok = self.fill_school()
        if ok:
            ok = self.fill_teachers_candidates(faker)
        if ok:
            ok = self.add_person_certificate(faker)
        if ok:
            ok = self.assign_cvs_to_candidates()
        if ok:
            ok = self.add_substitutions(faker)
        if ok:
            ok = self.fill_school_contacts(faker)
        if ok:
            ok = self.assign_teachers_to_schools(faker)
        if ok:
            ok = self.fill_classes()
        if ok:
            ok = self.fill_timetable_template(force_reset)
        if ok:
            ok = self.fill_person_subject(force_reset)
        if ok:
            ok = self.fill_timetable(force_reset)
        if ok:
            ok = self.assign_cvs_to_candidates()
        if ok:
            ok = self.fill_availabilities(force_reset)
        if ok:
            ok = self.fill_substitution_candidates(force_reset)
        if not ok:
            print("An error occurred while populating the data.")

