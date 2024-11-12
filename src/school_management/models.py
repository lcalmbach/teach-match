import os
import calendar
import locale

from django.db import models
from django.urls import reverse
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from enum import Enum

try:
    locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
except locale.Error:
    locale.setlocale(locale.LC_TIME, "C")


class CommunicationTypeEnum(Enum):
    BEWERBUNG = 1
    EINLADUNG = 2

class CommunicationResponseTypeEnum(Enum):
    BESTAETIGUNG = 1
    ABSAGE = 2
    ZUSAGE = 3
    OFFEN = 4


def default_communication_response_type():
    return CommunicationResponseType.objects.get(pk=CommunicationResponseTypeEnum.OFFEN.value)


def get_cv_upload_path(instance, filename):
    return os.path.join("cv", filename)


def get_default_time_of_day():
    try:
        return TimeOfDay.objects.get(pk=3).pk
    except TimeOfDay.DoesNotExist:
        return None


class CommunicationResponseType(models.Model):
    """Application, Invitation"""

    name = models.CharField(max_length=255, verbose_name="Name")
    description = models.TextField(verbose_name="Beschreibung", blank=True)

    class Meta:
        verbose_name = "AntwortTyp"
        verbose_name_plural = "Kommunikations Antworttypen"
        ordering = ["name"]

    def __str__(self):
        return self.name


class CommunicationType(models.Model):
    """Application, Invitation"""

    name = models.CharField(max_length=255, verbose_name="Name")
    description = models.TextField(verbose_name="Beschreibung", blank=True)

    class Meta:
        verbose_name = "Kommunikationsart"
        verbose_name_plural = "Kommunikationsarten"
        ordering = ["name"]

    def __str__(self):
        return self.name


class SubstitutionStatus(models.Model):
    """Status of a teacher substitution"""

    name = models.CharField(max_length=255, verbose_name="Name")
    description = models.TextField(verbose_name="Beschreibung", blank=True)

    class Meta:
        verbose_name = "Status der Stellvertretung"
        verbose_name_plural = "Status der Stellvertretungen"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Qualification(models.Model):
    """Abschluss, z.B. Lehrer, Sek1, Sek2, Matura, etc."""

    name = models.CharField(max_length=255, verbose_name="Qualifikation")

    class Meta:
        verbose_name = "Abschluss"
        verbose_name_plural = "Abschlüsse"
        ordering = ["name"]

    def __str__(self):
        return self.name


class SchoolYear(models.Model):
    year_start = models.SmallIntegerField(
        verbose_name="Jahr", default=datetime.now().year
    )
    start_date = models.DateField(verbose_name="Erster Schultag")
    end_date = models.DateField(verbose_name="Letzter Schultag")

    class Meta:
        verbose_name = "Schuljahr"
        verbose_name_plural = "Schuljahre"
        ordering = ["year_start"]

    def __str__(self):
        return self.year_start


class SubstitutionCause(models.Model):
    """cause for a teacher substitution"""

    name = models.CharField(max_length=255, verbose_name="Name")

    class Meta:
        verbose_name = "Code für Abwesenheitsgrund"
        verbose_name_plural = "Codes für Abwesenheitsgrund"
        ordering = ["name"]

    def __str__(self):
        return self.name


class SchoolPersonRole(models.Model):
    """Schulleitung, Lehrer, etc."""

    name = models.CharField(max_length=255, verbose_name="Name")

    class Meta:
        verbose_name = "Rolle in Schule"
        verbose_name_plural = "Rollen in Schule"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Location(models.Model):
    """Basel, Riehen, Bettingen"""

    name = models.CharField(max_length=255, verbose_name="Name")

    class Meta:
        verbose_name = "Ort"
        verbose_name_plural = "Orte"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"


class Gender(models.Model):
    """not sure if needed, not used yet for person model"""

    name = models.CharField(max_length=255, verbose_name="Geschlecht")

    class Meta:
        verbose_name = "Geschlecht"
        verbose_name_plural = "Geschlechter"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Certificate(models.Model):
    """Lehrer, Sek1, Sek2, Matura, etc."""

    name = models.CharField(max_length=255, verbose_name="Name")

    class Meta:
        verbose_name = "Abschluss"
        verbose_name_plural = "Abschlüsse"
        ordering = ["name"]

    def __str__(self):
        return self.name


class TimeOfDay(models.Model):
    """AM PM"""

    name = models.CharField(max_length=255, verbose_name="Tageszeit")

    class Meta:
        verbose_name = "Vormittag/Nachmittag"
        verbose_name_plural = "Vormittag/Nachmittag"
        ordering = ["-name"]

    def __str__(self):
        return self.name


class DayOfWeek(models.Model):
    """Monday, Tuesday, etc."""

    name = models.CharField(max_length=255, verbose_name="Wochentag")
    name_short = models.CharField(max_length=255, verbose_name="Kürzel")

    class Meta:
        verbose_name = "Wochentag"
        verbose_name_plural = "Wochentage"
        ordering = ["id"]

    def __str__(self):
        return self.name


class Period(models.Model):
    """0730-815, 0830-0915 etc."""

    start_time = models.TimeField(verbose_name="Start Time")
    end_time = models.TimeField(verbose_name="End Date")
    time_of_day = models.ForeignKey(
        TimeOfDay, on_delete=models.CASCADE, verbose_name="Tageszeit"
    )
    # day_of_week = models.ForeignKey(
    #    DayOfWeek, on_delete=models.CASCADE, verbose_name="Wochentag"
    # )

    class Meta:
        verbose_name = "Periode"
        verbose_name_plural = "Perioden"
        ordering = ["start_time"]

    def __str__(self):
        return f"{self.start_time} - {self.end_time}"


class Level(models.Model):
    """Sek1, Sek2, Kindergarten, Primarschule, etc.. used in school model"""

    name = models.CharField(max_length=255, verbose_name="Stufen-Name")
    name_short = models.CharField(max_length=255, verbose_name="Kurz-Name", blank=True)
    cycle = models.IntegerChoices("Zyklus", "1 2 3 4")
    cycle_name = models.CharField(
        max_length=255, verbose_name="Zyklus-Name", blank=True
    )
    cycle_name_short = models.CharField(
        max_length=255, verbose_name="Kurz-Zyklus-Name", blank=True
    )
    order = models.IntegerField(verbose_name="Reihenfolge", default=1)

    class Meta:
        verbose_name = "Stufe"
        verbose_name_plural = "Stufen"
        ordering = ["name"]

    def __str__(self):
        return self.name


# http://www.gewerbeschule.ch/agsbs/downloads/vk.pdf
class Subject(models.Model):
    """Mathematik, Deutsch, Englisch, etc."""

    name = models.CharField(max_length=255, verbose_name="Name")
    name_short = models.CharField(max_length=255, verbose_name="Kürzel", blank=True)
    description = models.TextField(verbose_name="Description", blank=True)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, verbose_name="Stufe")

    class Meta:
        verbose_name = "Fach"
        verbose_name_plural = "Fächer"
        ordering = ["name"]

    def __str__(self):
        return self.name


class School(models.Model):
    """Schule, Schulhaus, etc."""

    name = models.CharField(max_length=255, verbose_name="Standort")
    level = models.ForeignKey(
        Level,
        on_delete=models.CASCADE,
        verbose_name="Stufe",
        related_name="levels",
        default=1,
    )
    address = models.CharField(max_length=255, verbose_name="Adresse")
    url = models.URLField(verbose_name="Webseite", blank=True)
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        verbose_name="Ort",
        related_name="locations",
        default=1,
    )
    plz = models.IntegerField(verbose_name="Postleitzahl", default=4000)
    email = models.EmailField(verbose_name="Email", blank=True, max_length=255)
    phone_number = models.CharField(
        verbose_name="Telefonnummer", blank=True, max_length=255
    )
    mobile = models.CharField(verbose_name="Mobile", blank=True, max_length=255)

    class Meta:
        verbose_name = "Standort"
        verbose_name_plural = "Standorte"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Person(models.Model):
    """teacher, deputies and managers of the school"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    initials = models.CharField(max_length=255, verbose_name="Kürzel", blank=True)
    first_name = models.CharField(max_length=255, verbose_name="Vorname")
    last_name = models.CharField(max_length=255, verbose_name="Nachname")
    email = models.EmailField(verbose_name="Email", blank=True)
    phone_number = models.CharField(
        max_length=20, verbose_name="Telefonnummer", blank=True
    )
    year_of_birth = models.CharField(
        max_length=255, verbose_name="Jahrgang", blank=True
    )
    # cv_text = models.TextField(verbose_name="CV Text", blank=True)
    # cv_file = models.FileField(verbose_name="CV Datei", blank=True, upload_to=get_cv_upload_path)
    is_teacher = models.BooleanField(verbose_name="LehrerIn", default=False)
    is_candidate = models.BooleanField(
        verbose_name="KandidatIn für Stellvertretung", default=False
    )
    is_manager = models.BooleanField(
        verbose_name="Leitung/Administration", default=False
    )
    send_email = models.BooleanField(
        verbose_name="Kommunikation mit Email erwünscht", default=True
    )
    send_sms = models.BooleanField(
        verbose_name="Kommunikation mit SMS erwünscht", default=True
    )

    gender = models.ForeignKey(
        Gender,
        verbose_name="Geschlecht",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    available_from_date = models.DateField(
        verbose_name="Verfügbar von", blank=True, null=True
    )
    available_to_date = models.DateField(
        verbose_name="Verfügbar bis", blank=True, null=True
    )
    availability_mo_am = models.BooleanField(
        verbose_name="Montag Vormittag", default=False
    )
    availability_tu_am = models.BooleanField(
        verbose_name="Dienstag Vormittag", default=False
    )
    availability_we_am = models.BooleanField(
        verbose_name="Mittwoch Vormittag", default=False
    )
    availability_th_am = models.BooleanField(
        verbose_name="Donnerstag Vormittag", default=False
    )
    availability_fr_am = models.BooleanField(
        verbose_name="Freitag Vormittag", default=False
    )
    availability_mo_pm = models.BooleanField(
        verbose_name="Montag Nachmittag", default=False
    )
    availability_tu_pm = models.BooleanField(
        verbose_name="Dienstag Nachmittag", default=False
    )
    availability_we_pm = models.BooleanField(
        verbose_name="Mittwoch Nachmittag", default=False
    )
    availability_th_pm = models.BooleanField(
        verbose_name="Donnerstag Nachmittag", default=False
    )
    availability_fr_pm = models.BooleanField(
        verbose_name="Freitag Nachmittag", default=False
    )
    availability_comment = models.TextField(
        max_length=500, verbose_name="Bemerkungen zur Verfügbarkeit", blank=True
    )
    description = models.TextField(
        max_length=500, verbose_name="Bemerkungen", blank=True
    )

    notify_mail_flag = models.BooleanField(
        verbose_name="Benachrichtigung per Mail", default=False
    )
    notify_sms_flag = models.BooleanField(
        verbose_name="Benachrichtigung per SMS", default=False
    )

    subjects = models.ManyToManyField(
        "Subject", related_name="person_subjects", blank=True
    )  # Many-to-many relationship

    @property
    def formal_salutation(self):
        if self.gender.id == 1:
            return f"Sehr geehrter Herr {self.last_name}"
        else:
            return f"Sehr geehrte Frau {self.last_name}"

    @property
    def informal_salutation(self):
        if self.gender.id == 1:
            return f"Lieber {self.first_name}"
        else:
            return f"Liebe {self.first_name}"

    @property
    def fullname(self):
        return f"{self.last_name} {self.first_name}"

    @property
    def first_last_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Person"
        verbose_name_plural = "Personen"
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.year_of_birth}"


class Semester(models.Model):
    """Semester, e.g. HS2021, FS2022"""

    name = models.CharField(max_length=255, verbose_name="Name")
    start_date = models.DateField(verbose_name="Start Date")
    end_date = models.DateField(verbose_name="End Date")

    class Meta:
        verbose_name = "Semester"
        verbose_name_plural = "Semester"
        ordering = ["name"]

    def __str__(self):
        return self.name


class TeacherManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_teacher=True)


class Teacher(Person):
    objects = TeacherManager()

    class Meta:
        proxy = True

    def get_unique_subjects(self):
        # Get the unique subject objects related to lessons taught by this teacher
        unique_subject_ids = (
            Timetable.objects.filter(teacher=self)
            .values_list("subject", flat=True)
            .distinct()
        )
        unique_subjects = Subject.objects.filter(id__in=unique_subject_ids)
        return unique_subjects

    def get_unique_classes(self):
        # Get the unique class objects related to lessons taught by this teacher
        unique_class_ids = (
            Timetable.objects.filter(teacher=self)
            .values_list("school_class", flat=True)
            .distinct()
        )
        unique_classes = SchoolClass.objects.filter(id__in=unique_class_ids)
        return unique_classes

    def get_unique_days(self):
        # Unique Tage an denen der Lehrer arbeitet
        unique_day_numbers = (
            Timetable.objects.filter(teacher=self)
            .values_list("day", flat=True)
            .distinct()
            .order_by("day")
        )
        unique_day_names = [calendar.day_name[day] for day in unique_day_numbers]
        return unique_day_names

    def get_school(self):
        # Erste Schule, an der der Lehrer unterrichtet
        school = (
            Timetable.objects.filter(teacher=self)
            .values_list("school", flat=True)
            .distinct()
            .first()  # Get the first school ID
        )
        return School.objects.get(pk=school) if school else None


class CandidateManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_candidate=True)


class Candidate(Person):
    objects = CandidateManager()

    class Meta:
        proxy = True


class Substitution(models.Model):
    """Time frame for a teacher substitution"""

    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name="substitution_schools",
        verbose_name="Schule",
    )
    teacher = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="teacher_substitutions",
        verbose_name="Lehrkraft",
    )
    start_date = models.DateField(verbose_name="Fällt aus von")
    end_date = models.DateField(verbose_name="Fällt aus bis")
    cause = models.ForeignKey(
        SubstitutionCause(),
        on_delete=models.CASCADE,
        related_name="substitution_causes",
        verbose_name="Begründung",
        default=1,
    )
    partial_substitution_possible = models.BooleanField(
        verbose_name="Teilübernahme möglich", default=False
    )
    comment_subsitution = models.TextField(
        verbose_name="Anmerkung zum Vikariat", blank=True, max_length=500
    )
    comment_class = models.TextField(
        verbose_name="Anmerkung zur Klasse", blank=True, max_length=500
    )
    minimum_qualification = models.ForeignKey(
        Qualification,
        on_delete=models.CASCADE,
        related_name="substitution_certificates",
        verbose_name="Mindestabschluss",
        default=1,
    )
    # für die Anzeige
    classes = models.TextField(verbose_name="Klassen", blank=True, max_length=500)
    levels = models.TextField(verbose_name="Stufen", blank=True, max_length=500)
    subjects = models.TextField(verbose_name="Fächer", blank=True, max_length=500)
    summary = models.TextField(
        verbose_name="Zusammenfassung", blank=True, max_length=1000
    )

    mo_am = models.BooleanField(verbose_name="Montag Vormittag", default=False)
    mo_pm = models.BooleanField(verbose_name="Montag Nachmittag", default=False)
    tu_am = models.BooleanField(verbose_name="Dienstag Vormittag", default=False)
    tu_pm = models.BooleanField(verbose_name="Dienstag Nachmittag", default=False)
    we_am = models.BooleanField(verbose_name="Mittwoch Vormittag", default=False)
    we_pm = models.BooleanField(verbose_name="Mittwoch Nachmittag", default=False)
    th_am = models.BooleanField(verbose_name="Donnerstag Vormittag", default=False)
    th_pm = models.BooleanField(verbose_name="Donnerstag Nachmittag", default=False)
    fr_am = models.BooleanField(verbose_name="Freitag Vormittag", default=False)
    fr_pm = models.BooleanField(verbose_name="Freitag Nachmittag", default=False)

    selection_comment = models.TextField(
        verbose_name="Kommentar zur Besetzung", blank=True, max_length=500
    )
    status = models.ForeignKey(
        SubstitutionStatus,
        on_delete=models.SET_DEFAULT,
        default=1,
        related_name="substitution_status",
        verbose_name="Status Besetzung Vikariat",
    )
    created_timestamp = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = "Stellvertretung"
        verbose_name_plural = "Stellvertretungen"

    def url(self):
        return reverse("school_management:substitution_detail", args=[self.pk])

    def __str__(self):
        return f"{self.teacher.fullname} - {self.start_date} - {self.end_date}"


class SchoolClass(models.Model):
    """Klasse, e.g. 1A, 2B, etc."""

    school = models.ForeignKey(
        School, on_delete=models.CASCADE, related_name="class_schools", default=1
    )
    name = models.CharField(max_length=255, verbose_name="Name")
    year = models.IntegerField(verbose_name="Jahr", default=1)
    level = models.ForeignKey(
        Level, on_delete=models.CASCADE, related_name="class_levels"
    )
    # contact_person = models.ForeignKey(
    #     Person, on_delete=models.CASCADE, related_name="class_persons"
    # )
    school_year = models.IntegerField(verbose_name="Schuljahr", default=1)

    class Meta:
        verbose_name = "Klasse"
        verbose_name_plural = "Klassen"

    def __str__(self):
        return f"{self.school.name}, Klasse {self.name}"


class Timetable(models.Model):
    """timetable template for a teacher: all periods for a week. the tempalte is used to create the timetable"""

    semester = models.ForeignKey(
        Semester, on_delete=models.CASCADE, related_name="timetable_semesters"
    )
    teacher = models.ForeignKey(
        Person, on_delete=models.CASCADE, related_name="lessons_template_teachers"
    )
    school = models.ForeignKey(
        School, on_delete=models.CASCADE, related_name="lesson_template_schools"
    )
    period = models.ForeignKey(
        Period, on_delete=models.CASCADE, related_name="lesson_template_periods"
    )
    day = models.ForeignKey(
        DayOfWeek, on_delete=models.CASCADE, related_name="lesson_template_days"
    )
    school_class = models.ForeignKey(
        SchoolClass,
        on_delete=models.CASCADE,
        related_name="lesson_template_school_classes",
    )
    frequency = models.IntegerField(verbose_name="Alle n Wochen", default=1)
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name="lesson_template_subjects"
    )

    class Meta:
        verbose_name = "Lektion-Template"
        verbose_name_plural = "Lektion-Templates"

    def __str__(self):
        return f"{self.day.name_short} {self.period} {self.subject.name}"


class SubstitutionCandidate(models.Model):
    """Candidates with available for a substitution period and proficiency with the subject of the lessons
    The rating is a number from 1 to 100.
    """

    substitution = models.ForeignKey(
        "Substitution", on_delete=models.CASCADE, related_name="substitution_candidates"
    )
    candidate = models.ForeignKey(
        "Person",
        on_delete=models.CASCADE,
        related_name="substitution_candidates_persons",
    )
    matching_half_days = models.IntegerField(
        verbose_name="Übereinstimmende Halbtage", default=0
    )
    matching_subjects = models.IntegerField(
        verbose_name="Übereinstimmende Fächer", default=0
    )
    num_experiences = models.IntegerField(verbose_name="Anzahl Erfahrungen", default=0)
    num_experiences_in_school = models.IntegerField(
        verbose_name="Anzahl Erfahrungen in Schule", default=0
    )
    num_experiences_with_class = models.IntegerField(
        verbose_name="Anzahl Erfahrungen mit Klasse", default=0
    )
    num_experiences_with_subjects = models.IntegerField(
        verbose_name="Anzahl Erfahrungen mit Fach", default=0
    )
    rating = models.IntegerField(verbose_name="Bewertung", default=1)
    comments = models.TextField(verbose_name="Bemerkungen", blank=True)
    selected = models.BooleanField(verbose_name="Ausgewählt", default=False)
    invited_date = models.DateField(
        verbose_name="Einladungsdatum", blank=True, null=True
    )
    selected_date = models.DateField(verbose_name="Zusage", blank=True, null=True)
    accepted_date = models.DateField(
        verbose_name="Bestätigung am", blank=True, null=True
    )
    record_created_date = models.DateField(
        default=timezone.now, verbose_name="Erstellt am"
    )

    class Meta:
        verbose_name = "Vertretung-KandidatIn"
        verbose_name_plural = "Vertretung-Kandidaten"

    def __str__(self):
        return f"{self.candidate.fullname} - {self.rating}"


class Vacation(models.Model):
    """Teacher vacation"""

    name = models.CharField(max_length=100, verbose_name="Bezeichnung")
    date_from = models.DateField(verbose_name="Von", default=timezone.now)
    date_to = models.DateField(verbose_name="Bis", default=timezone.now)
    timeofday = models.ForeignKey(
        TimeOfDay,
        on_delete=models.CASCADE,
        related_name="vacation_template_time_of_day",
        default=get_default_time_of_day,
    )

    class Meta:
        verbose_name = "Ferien"
        verbose_name_plural = "Ferien"

    def __str__(self):
        return f"{self.name} {self.date_from} - {self.date_to}"


class VacationDay(models.Model):
    """Teacher vacation"""

    date = models.DateField(verbose_name="Datum", default=timezone.now)
    timeofday = models.ForeignKey(
        TimeOfDay,
        on_delete=models.CASCADE,
        related_name="vacation_time_of_day",
        default=get_default_time_of_day,
    )
    vacation = models.ForeignKey(
        Vacation, on_delete=models.CASCADE, related_name="vacation_templates"
    )

    def __str__(self):
        return f"{self.date} - {self.vacation.name}"


class Communication(models.Model):
    substitution = models.ForeignKey(
        Substitution, on_delete=models.CASCADE, related_name="substitution"
    )
    candidate = models.ForeignKey(
        Candidate, on_delete=models.CASCADE, related_name="candidate"
    )
    type = models.ForeignKey(
        CommunicationType, on_delete=models.CASCADE, related_name="communication_type"
    )
    request_date = models.DateField(verbose_name="Gesendet am", default=timezone.now)
    request_text = models.TextField(verbose_name="Anfrage", blank=True, max_length=500)
    response_text = models.TextField(verbose_name="Antwort", blank=True, max_length=500)
    response_date = models.DateField(verbose_name="Antwort am", blank=True, null=True, default=timezone.now)
    response_type = models.ForeignKey(
        CommunicationResponseType,
        on_delete=models.CASCADE,
        related_name="communication_response_type",
        null=True,
        blank=True,
        default=default_communication_response_type,
    )
    comments = models.TextField(verbose_name="Kommentar", blank=True, max_length=500)
    rating = models.IntegerField(verbose_name="Bewertung", default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])


    def subject(self):
        return f"Stellvertretung {self.substitution.id}, {self.substitution.school.name}, {self.substitution.start_date.strftime('%d.%m.%Y')}-{self.substitution.end_date.strftime('%d.%m.%Y')} {self.candidate.fullname}"

    
    def __str__(self):
        return f"{self.request_date} {self.candidate.fullname}"


class ApplicationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type_id=1)


class Application(Communication):
    objects = ApplicationManager()

    class Meta:
        proxy = True

    def star_rating(self):
        if self.rating is None:
            return "No rating"
        return "★" * self.rating + "☆" * (5 - self.rating)

    def __str__(self):
        return f"{self.request_date} {self.candidate.fullname}"

class InvitationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type_id=2)


class Invitation(Communication):
    objects = InvitationManager()

    class Meta:
        proxy = True
