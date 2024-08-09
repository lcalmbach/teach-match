from datetime import datetime, timedelta
from django.apps import apps
import os
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from .models import SubstitutionCandidate

def get_week_days(start_date, end_date):
    """
    Returns a list of unique weekdays between the given start_date and end_date (inclusive).

    Args:
        start_date (datetime.date): The start date.
        end_date (datetime.date): The end date.

    Returns:
        list: A list of unique weekdays (0-6, where 0 represents Monday and 6 represents Sunday).

    """
    days = []
    current_date = start_date
    while current_date <= end_date:
        if current_date.weekday() not in days:
            days.append(current_date.weekday())
        current_date += timedelta(days=1)
    return days


class SubstitutionHelper:
    def __init__(self, substitution) -> None:
        self.substitution = substitution
        self.days_in_substitution = []
        self.lessons = []
        self.classes = []
        self.levels = []
        self.canidates = []
        self.mo_am = False
        self.tu_am = False
        self.we_am = False
        self.th_am = False
        self.fr_am = False
        self.mo_pm = False
        self.tu_pm = False
        self.we_pm = False
        self.th_pm = False
        self.fr_pm = False
        self.init()

    def get_matching_half_days(self, candidate):
        result = 0
        result += 1 if self.substitution.mo_am and candidate.availability_mo_am else 0 
        result += 1 if self.substitution.mo_pm and candidate.availability_mo_pm else 0 
        result += 1 if self.substitution.tu_am and candidate.availability_tu_am else 0 
        result += 1 if self.substitution.tu_pm and candidate.availability_tu_pm else 0 
        result += 1 if self.substitution.we_am and candidate.availability_we_am else 0 
        result += 1 if self.substitution.we_pm and candidate.availability_we_pm else 0 
        result += 1 if self.substitution.th_am and candidate.availability_th_am else 0 
        result += 1 if self.substitution.th_pm and candidate.availability_th_pm else 0 
        result += 1 if self.substitution.fr_am and candidate.availability_fr_am else 0 
        result += 1 if self.substitution.fr_pm and candidate.availability_fr_pm else 0 

        return result

    def get_half_days(self):
        result = 0
        result += 1 if self.substitution.mo_am else 0 
        result += 1 if self.substitution.mo_pm else 0 
        result += 1 if self.substitution.tu_am else 0 
        result += 1 if self.substitution.tu_pm else 0 
        result += 1 if self.substitution.we_am else 0 
        result += 1 if self.substitution.we_pm else 0 
        result += 1 if self.substitution.th_am else 0 
        result += 1 if self.substitution.th_pm else 0 
        result += 1 if self.substitution.fr_am else 0 
        result += 1 if self.substitution.fr_pm else 0 

        return result
    
    def init(self):
        Lesson = apps.get_model("school_management", "Timetable")
        SchoolClass = apps.get_model("school_management", "SchoolClass")

        self.days_in_substitution = list(
            get_week_days(self.substitution.start_date, self.substitution.end_date)
        )
        self.lessons = Lesson.objects.filter(
            teacher=self.substitution.teacher,
            day__in=self.days_in_substitution,
        ).order_by('day__id', 'period__id')
        self.classes = SchoolClass.objects.filter(
            id__in=self.lessons.values_list("school_class_id", flat=True)
        )
        self.levels = list(set([cls.level for cls in self.classes]))
        self.subjects = list(set([lesson.subject for lesson in self.lessons]))
        self.days = self.get_number_of_days_in_period()
        self.candidates = self.get_candidates()

    def get_number_of_days_in_period(self):
        """returns the number of week days between two dates"""
        days = 0
        current_date = self.substitution.start_date
        while current_date <= self.substitution.end_date:
            if current_date.weekday() < 5:
                days += 1
            current_date += timedelta(days=1)
        return days

    def get_summary(self):
        text = f"Von {self.substitution.start_date.strftime('%d.%m.%y')} bis {self.substitution.end_date.strftime('%d.%m.%y')}, insgesamt {len(self.lessons)} Wochenlektionen. "
        if not self.substitution.comment_subsitution is None:
            text += f"\n{self.substitution.comment_subsitution}."
        if not self.substitution.comment_class is None:
            text += f"\n{self.substitution.comment_class}."
        return text

    def get_halfdays(self):
        periods = [
                    {"d": lesson.day_id, "t": lesson.period.time_of_day_id}
                    for lesson in self.lessons
        ]
        result = {
            'mo_am': {"d": 0, "t": 0} in periods,
            'mo_pm': {"d": 0, "t": 1} in periods,
            'tu_am': {"d": 1, "t": 0} in periods,
            'tu_pm': {"d": 1, "t": 1} in periods,
            'we_am': {"d": 2, "t": 0} in periods,
            'we_pm': {"d": 2, "t": 1} in periods,
            'th_am': {"d": 3, "t": 0} in periods,
            'th_pm': {"d": 3, "t": 1} in periods,
            'fr_am': {"d": 4, "t": 0} in periods,
            'fr_pm': {"d": 4, "t": 1} in periods,
        }
        return result

    def get_candidates(self):
        def assign_rating(number, max_number, max_rating=20):
            if number >= max_number:
                return max_rating
            return int(number / max_number * max_rating)

        SubstitutionCandidate.objects.filter(substitution=self.substitution).delete()
        candidate = apps.get_model("school_management", "Candidate")
        substitution_candidate = apps.get_model("school_management", "SubstitutionCandidate")
        candidates = candidate.objects.filter(
            available_from_date__lt=self.substitution.start_date,
            available_to_date__gt=self.substitution.end_date,
        )
        result = []
        half_days = self.get_half_days()
        for c in candidates:
            matching_half_days = self.get_matching_half_days(c)
            if matching_half_days > 0:
                num_experiences = SubstitutionCandidate.objects.filter(candidate=c, accepted_date__isnull=False).count()

                num_experiences_in_school = SubstitutionCandidate.objects.filter(candidate=c, accepted_date__isnull=False, substitution__school=self.substitution.school).count()
                # num_experiences_with_class = random.randint(1, 2)
                # num_experiences_with_subjects = num_experiences_in_school
                
                rating = matching_half_days / half_days * 50 if matching_half_days > 0 else 0
                rating += assign_rating(num_experiences, 6, 25)
                rating += assign_rating(num_experiences_in_school, 3, 25)
                #rating += assign_rating(num_experiences_with_class, 3, 10) 
                #rating += assign_rating(num_experiences_with_subjects, 2, 10)

                sc = substitution_candidate.objects.create(
                    candidate=c,
                    substitution=self.substitution,
                    matching_half_days=matching_half_days,
                    num_experiences=num_experiences,
                    num_experiences_in_school=num_experiences_in_school,
                    #num_experiences_with_class=num_experiences_with_class,
                    #num_experiences_with_subjects=num_experiences_with_subjects,
                    rating=rating
                )
                result.append(sc)
        return result

    def send_email(self, subject, body):
        # Gmail credentials
        gmail_user = os.getenv('GMAIL_USER')
        gmail_password = os.getenv('GMAIL_PASSWORD')

        # Create the email
        to_email = self.substitution.school.email
        msg = MIMEMultipart()
        msg['From'] = gmail_user
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        # Connect to the Gmail server
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(gmail_user, gmail_password)
            text = msg.as_string()
            print(gmail_user, to_email, text)
            server.sendmail(gmail_user, to_email, text)
            print('Email sent successfully')
        except Exception as e:
            print(f'Failed to send email: {e}')
        finally:
            server.quit()
            
    def assign_values(self):
        self.substitution.classes = ",".join([cls.name for cls in self.classes])
        self.substitution.levels = ",".join([lvl.name_short for lvl in self.levels])
        self.substitution.subjects = ",".join([sbj.name_short for sbj in self.subjects])
        # if self.substitution.summary is None or self.substitution.summary == "":
        self.substitution.summary = self.get_summary()
        self.substitution.subjects = ",".join([sbj.name_short for sbj in self.subjects])
        
        SubstitutionCandidate = apps.get_model("school_management", "SubstitutionCandidate")
        SubstitutionCandidate.objects.all().filter(substitution=self.substitution).delete()

        candidates = self.get_candidates()
        self.substitution.substitution_candidates.set(candidates)

        halfdays = self.get_halfdays()
        am_pm_keys = ["mo_am", "tu_am", "we_am", "th_am", "fr_am", "mo_pm", "tu_pm", "we_pm", "th_pm", "fr_pm"]
        for key in am_pm_keys:
            setattr(self.substitution, key, halfdays.get(key))

        return self.substitution