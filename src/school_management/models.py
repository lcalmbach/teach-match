from django.db import models
from datetime import datetime

class SchoolYear(models.Model):
    year_start = models.SmallIntegerField(verbose_name="Jahr", default=datetime.now().year),
    start_date = models.DateField(verbose_name="Erster Schultag"),
    end_date = models.DateField(verbose_name="Letzter Schultag")

    def __str__(self):
        return self.year_start
    

class SubstitutionCause(models.Model):
    """cause for a teacher substitution"""

    name = models.CharField(max_length=255, verbose_name="Name")

    def __str__(self):
        return self.name

class SchoolPersonRole(models.Model):
    """Schulleitung, Lehrer, etc."""

    name = models.CharField(max_length=255, verbose_name="Name")

    def __str__(self):
        return self.name


class Location(models.Model):
    """Basel, Riehen, Bettingen"""

    name = models.CharField(max_length=255, verbose_name="Name")

    def __str__(self):
        return f"{self.name}"


class Gender(models.Model):
    """not sure if needed, not used yet for person model"""

    name = models.CharField(max_length=255, verbose_name="Geschlecht")

    def __str__(self):
        return self.name


class Certificate(models.Model):
    """Lehrer, Sek1, Sek2, Matura, etc."""

    name = models.CharField(max_length=255, verbose_name="Name")

    def __str__(self):
        return self.name


class TimeOfDay(models.Model):
    """AM PM"""

    name = models.CharField(max_length=255, verbose_name="Tageszeit")

    def __str__(self):
        return self.name


class DayOfWeek(models.Model):
    """Monday, Tuesday, etc."""

    name = models.CharField(max_length=255, verbose_name="Wochentag")
    short_name = models.CharField(max_length=255, verbose_name="Kürzel")

    def __str__(self):
        return self.name


class Period(models.Model):
    """0730-815, 0830-0915 etc."""

    start_time = models.TimeField(verbose_name="Start Time")
    end_time = models.TimeField(verbose_name="End Date")
    time_of_day = models.ForeignKey(
        TimeOfDay, on_delete=models.CASCADE, verbose_name="Tageszeit"
    )
    #day_of_week = models.ForeignKey(
    #    DayOfWeek, on_delete=models.CASCADE, verbose_name="Wochentag"
    #)
    
    def __str__(self):
        return f"{self.start_time} - {self.end_time}"


class Course(models.Model):
    """grouping of subjects, e.g."""

    name = models.CharField(max_length=255, verbose_name="Kursname")
    description = models.TextField(verbose_name="Description", blank=True)

    def __str__(self):
        return self.name


class Level(models.Model):
    """Sek1, Sek2, Kindergarten, Primarschule, etc.. used in school model"""

    name = models.CharField(max_length=255, verbose_name="Stufen-Name")

    def __str__(self):
        return self.name


# http://www.gewerbeschule.ch/agsbs/downloads/vk.pdf
class Subject(models.Model):
    """Mathematik, Deutsch, Englisch, etc."""

    name = models.CharField(max_length=255, verbose_name="Name")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Kurs")
    description = models.TextField(verbose_name="Description", blank=True)
    school_year = models.IntegerField(verbose_name="Schuljahr", default=1)

    def __str__(self):
        return self.name


class School(models.Model):
    """Schule, Schulhaus, etc."""

    name = models.CharField(max_length=255, verbose_name="Schule")
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

    def __str__(self):
        return self.name


class Person(models.Model):
    """teacher, deputies and managers of the school"""

    first_name = models.CharField(max_length=255, verbose_name="Vorame")
    last_name = models.CharField(max_length=255, verbose_name="Nachname")
    email = models.EmailField(verbose_name="Email", blank=True)
    phone_number = models.CharField(
        max_length=20, verbose_name="Phone Number", blank=True
    )
    year_of_birth = models.CharField(
        max_length=255, verbose_name="Geburtsjahr", blank=True
    )
    cv_text = models.TextField(verbose_name="CV Text", blank=True)
    cv_file = models.FileField(verbose_name="Curriculum", blank=True, upload_to="cv/")
    is_teacher = models.BooleanField(verbose_name="Lehrer", default=False)
    is_candidate = models.BooleanField(verbose_name="Kandidat", default=False)
    is_leitung = models.BooleanField(
        verbose_name="Leitung/Administration",
        default=False
    )
    years_of_experience = models.IntegerField(
        verbose_name="Erfahrung", blank=True, default=1
    )
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE, verbose_name="Geschlecht", default=1)
    description = models.TextField(
        max_length=500, verbose_name="Bemerkungen", blank=True
    )

    @property
    def fullname(self):
        return f"{self.last_name} {self.first_name}"
    
    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.year_of_birth}"


class SchoolPerson(models.Model):
    """persons related to a school, e.g. school director, teachers etc."""

    school = models.ForeignKey(
        School, on_delete=models.CASCADE, related_name="school_person_schools"
    )
    person = models.ForeignKey(
        Person, on_delete=models.CASCADE, related_name="school_persons"
    )
    role = models.ForeignKey(
        SchoolPersonRole, on_delete=models.CASCADE, related_name="school_person_roles"
    )
    description = models.TextField(verbose_name="Bemerkungen", blank=True)

    def __str__(self):
        return f"{self.person.last_name} {self.person.first_name} {self.role.name}"


class PersonCertificate(models.Model):
    """Certificates for deputies and teachers of the school"""

    person = models.ForeignKey(
        Person, on_delete=models.CASCADE, related_name="certificates"
    )
    certificate = models.ForeignKey(
        Certificate, on_delete=models.CASCADE, related_name="candidates_person"
    )
    year = models.CharField(max_length=255, verbose_name="Jahr", blank=True, null=True)
    
    def __str__(self):
        return f"{self.person.name} - {self.certificate.name} - {self.year}"


class PersonSubject(models.Model):
    """
    Subjects for deputies and teachers of the school. experience goes from 1: only studied to 5:
    teaching experience
    """

    person = models.ForeignKey(
        Person, on_delete=models.CASCADE, related_name="personsubject_persons"
    )
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name="personsubject_subjects"
    )
    experience = models.IntegerField(verbose_name="Erfahrung", blank=True, default=1)
    description = models.TextField(verbose_name="Description", blank=True, max_length=500)

    def __str__(self):
        return f"{self.person.fullname} - {self.subject.name} - {self.experience}"


class Substitution(models.Model):
    """Time frame for a teacher substitution"""

    teacher = models.ForeignKey(
        Person, on_delete=models.CASCADE, related_name="teacher_substitutions", verbose_name="Lehrkraft"
    )
    start_date = models.DateField(verbose_name="Fällt aus von")
    end_date = models.DateField(verbose_name="Fällt aus bis")
    start_period = models.ForeignKey(
        Period, on_delete=models.CASCADE, related_name="start_periods", verbose_name="Von Lektion"
    )
    end_period = models.ForeignKey(
        Period, on_delete=models.CASCADE, related_name="end_periods", verbose_name="Bis Lektion"
    )
    cause = models.ForeignKey(SubstitutionCause(), on_delete=models.CASCADE, related_name="substitution_causes", verbose_name="Begründung")
    description = models.TextField(verbose_name="Beschreibung", blank=True, max_length=500)
    
    def __str__(self):
        return f"{self.teacher.fullname} - {self.start_period.start_time} - {self.end_period.end_time}"


class Availability(models.Model):
    """Deputy candidate availability"""

    candidate = models.ForeignKey(
        Person, on_delete=models.CASCADE, related_name="availabilities", verbose_name="Kandidat*in"
    )
    date_from = models.DateField(verbose_name="Von")
    date_to = models.DateField(verbose_name="Bis")
    day_of_week = models.ForeignKey(DayOfWeek, on_delete=models.CASCADE, related_name="availabilities_days", blank=True, null=True)
    time_of_day = models.ForeignKey(TimeOfDay, on_delete=models.CASCADE, related_name="availabilities_time_of_day")
    
    def __str__(self):
        return f"{self.candidate.fullname} - {self.date_from} - {self.date_to}"


class SchoolClass(models.Model):
    """Klasse, e.g. 1A, 2B, etc."""
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="class_schools", default=1)
    name = models.CharField(max_length=255, verbose_name="Name")
    year = models.IntegerField(verbose_name="Jahr", default=1)
    level = models.ForeignKey(
        Level, on_delete=models.CASCADE, related_name="class_levels"
    )
    contact_person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="class_persons")
    school_year = models.IntegerField(verbose_name="Schuljahr", default=1)
    
    def __str__(self):
        return self.name


class LessonTemplate(models.Model):
    """timetable template for a teacher: all periods for a week. the tempalte is used to create the timetable"""

    teacher = models.ForeignKey(
        Person, on_delete=models.CASCADE, related_name="lessons_template_teachers"
    )
    school = models.ForeignKey(
        School, on_delete=models.CASCADE, related_name="lesson_template_schools"
    )
    period = models.ForeignKey(
        Period, on_delete=models.CASCADE, related_name="lesson_template_periods"
    )
    day = models.ForeignKey(DayOfWeek, on_delete=models.CASCADE, related_name="lesson_template_days")
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, related_name="lesson_template_school_classes")
    frequency = models.IntegerField(verbose_name="Alle n Wochen", default=1)
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name="lesson_template_subjects"
    )

    def __str__(self):
        return F"{self.day.short_name} {self.period} {self.subject.name}"



class Lesson(models.Model):
    """timetable for a teacher"""

    teacher = models.ForeignKey(
        Person, on_delete=models.CASCADE, related_name="lesson_teachers"
    )
    school = models.ForeignKey(
        School, on_delete=models.CASCADE, related_name="lesson_schools"
    )
    date = models.DateField(verbose_name="Date")
    period = models.ForeignKey(
        Period, on_delete=models.CASCADE, related_name="lesson_periods"
    )
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, related_name="lesson_school_classes", default=1)
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name="subjects"
    )

    def __str__(self):
        return f"{self.teacher.name} - {self.day} - {self.period.start_time} - {self.period.end_time}"


class SubstitutionPeriod(models.Model):
    substitution = models.ForeignKey(
        Substitution, on_delete=models.CASCADE, related_name="substitution_subjects"
    )
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name="substitution_lessons"
    )
    # deptuty is initialized blank and must be filled in a second step
    deputy = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="substitution_deputies", blank=True, null=True)

    @classmethod
    def create_substitution_periods(cls, substitution, lesson_qs):
        """
        Create SubstitutionPeriod instances for each lesson in the queryset lesson_qs
        for the given substitution.
        """
        substitution_periods = []
        for lesson in lesson_qs:
            substitution_period = cls(substitution=substitution, lesson=lesson)
            substitution_periods.append(substitution_period)
        cls.objects.bulk_create(substitution_periods)
        
    def __str__(self):
        return f"{self.lesson.subject.name}"


class VacationTemplate(models.Model):
    """Teacher vacation"""

    date_from = models.DateField(verbose_name="Von")
    date_to = models.DateField(verbose_name="Bis")
    timeofday = models.ForeignKey(TimeOfDay, on_delete=models.CASCADE, related_name="vacation_time_of_day")
    description = models.TextField(verbose_name="Bemerkungen", blank=True)

    def __str__(self):
        return f"{self.date_from} - {self.date_to}"


class VacationDay(models.Model):
    """Teacher vacation"""

    date = models.DateField(verbose_name="Datum")
    vacation = models.ForeignKey(VacationTemplate, on_delete=models.CASCADE, related_name="vacation_templates")

    def __str__(self):
        return f"{self.date} - {self.vacation.description}"