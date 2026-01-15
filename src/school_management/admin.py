from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Category, Code,
    Gender, CommunicationResponseType, CommunicationType,
    SubstitutionStatus, SubstitutionCause, SchoolPersonRole,
    Certificate, DayPart, WeekDay, Location,
    Qualification, SchoolYear, TimePeriod, Level, Subject,
    Department, Semester, CustomUser, Teacher, Candidate,
    Substitution, SchoolClass, Timetable, SubstitutionLesson,
    SubstitutionCandidate, SubstitutionExecution,
    Vacation, SchoolDay, Communication, Application, Invitation
)


# ============= Master Data - Categories and Codes =============

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Code)
class CodeAdmin(admin.ModelAdmin):
    list_display = ('short_name', 'name', 'category', 'order')
    list_filter = ('category',)
    search_fields = ('name', 'short_name')
    ordering = ('category', 'order', 'name')


# Proxy model admins for specific code types
@admin.register(Gender)
class GenderAdmin(admin.ModelAdmin):
    list_display = ('short_name', 'name', 'order')
    ordering = ('order',)


@admin.register(CommunicationResponseType)
class CommunicationResponseTypeAdmin(admin.ModelAdmin):
    list_display = ('short_name', 'name', 'order')
    ordering = ('order',)


@admin.register(CommunicationType)
class CommunicationTypeAdmin(admin.ModelAdmin):
    list_display = ('short_name', 'name', 'order')
    ordering = ('order',)


@admin.register(SubstitutionStatus)
class SubstitutionStatusAdmin(admin.ModelAdmin):
    list_display = ('short_name', 'name', 'order')
    ordering = ('order',)


@admin.register(SubstitutionCause)
class SubstitutionCauseAdmin(admin.ModelAdmin):
    list_display = ('short_name', 'name', 'order')
    ordering = ('order',)


@admin.register(SchoolPersonRole)
class SchoolPersonRoleAdmin(admin.ModelAdmin):
    list_display = ('short_name', 'name', 'order')
    ordering = ('order',)


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('short_name', 'name', 'order')
    ordering = ('order',)


@admin.register(DayPart)
class DayPartAdmin(admin.ModelAdmin):
    list_display = ('short_name', 'name', 'order')
    ordering = ('order',)


@admin.register(WeekDay)
class WeekDayAdmin(admin.ModelAdmin):
    list_display = ('short_name', 'name', 'order')
    ordering = ('order',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('short_name', 'name', 'order')
    ordering = ('order',)


# ============= Other Master Data =============

@admin.register(Qualification)
class QualificationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(SchoolYear)
class SchoolYearAdmin(admin.ModelAdmin):
    list_display = ('year_start', 'start_date', 'end_date')
    list_filter = ('year_start',)
    ordering = ('-year_start',)


@admin.register(TimePeriod)
class TimePeriodAdmin(admin.ModelAdmin):
    list_display = ('code', 'day', 'start_time', 'end_time', 'time_of_day')
    list_filter = ('day',)
    ordering = ('day', 'start_time')


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_short', 'cycle_name', 'order')
    ordering = ('order',)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_short', 'level')
    list_filter = ('level',)
    search_fields = ('name', 'name_short')
    ordering = ('name',)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'level', 'location', 'email', 'phone_number')
    list_filter = ('level', 'location')
    search_fields = ('name', 'code', 'email')
    fieldsets = (
        ('Grundinformationen', {
            'fields': ('name', 'code', 'level', 'location')
        }),
        ('Adresse', {
            'fields': ('address',)
        }),
        ('Kontakt', {
            'fields': ('email', 'phone_number', 'mobile', 'url')
        }),
    )


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date')
    ordering = ('-start_date',)


# ============= Business Data - People =============

@admin.register(CustomUser)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'email', 'mobile', 'is_teacher', 'is_candidate', 'is_manager')
    list_filter = ('is_teacher', 'is_candidate', 'is_manager', 'gender')
    search_fields = ('first_name', 'last_name', 'email', 'employee_number')
    filter_horizontal = ('subjects',)
    
    fieldsets = (
        ('Persönliche Daten', {
            'fields': ('user', 'initials', 'employee_number', 'first_name', 'last_name', 
                      'gender', 'year_of_birth', 'email', 'mobile')
        }),
        ('Rollen', {
            'fields': ('is_teacher', 'is_candidate', 'is_manager')
        }),
        ('Verfügbarkeit - Zeitraum', {
            'fields': ('available_from_date', 'available_to_date')
        }),
        ('Verfügbarkeit - Vormittag', {
            'fields': ('availability_mo_am', 'availability_tu_am', 'availability_we_am', 
                      'availability_th_am', 'availability_fr_am')
        }),
        ('Verfügbarkeit - Nachmittag', {
            'fields': ('availability_mo_pm', 'availability_tu_pm', 'availability_we_pm', 
                      'availability_th_pm', 'availability_fr_pm')
        }),
        ('Fächer & Bemerkungen', {
            'fields': ('subjects', 'availability_comment', 'description')
        }),
        ('Benachrichtigungen', {
            'fields': ('notify_mail_flag', 'notify_sms_flag')
        }),
    )


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'email', 'mobile', 'initials')
    search_fields = ('first_name', 'last_name', 'email', 'initials')
    filter_horizontal = ('subjects',)


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'email', 'mobile', 'available_from_date', 'available_to_date')
    list_filter = ('available_from_date', 'available_to_date')
    search_fields = ('first_name', 'last_name', 'email')
    filter_horizontal = ('subjects',)


# ============= Substitutions =============

@admin.register(Substitution)
class SubstitutionAdmin(admin.ModelAdmin):
    list_display = ('ref_no', 'department', 'teacher', 'start_date', 'end_date', 'status', 'created_timestamp')
    list_filter = ('status', 'department', 'start_date', 'cause')
    search_fields = ('teacher__first_name', 'teacher__last_name', 'school__name')
    date_hierarchy = 'start_date'
    readonly_fields = ('created_timestamp', 'ref_no', 'url')
    
    fieldsets = (
        ('Grundinformationen', {
            'fields': ('department', 'teacher', 'start_date', 'end_date', 'cause', 'status')
        }),
        ('Details', {
            'fields': ('minimum_qualification', 'partial_substitution_possible', 
                      'comment_subsitution', 'comment_class')
        }),
        ('Verfügbarkeit - Vormittag', {
            'fields': ('mo_am', 'tu_am', 'we_am', 'th_am', 'fr_am')
        }),
        ('Verfügbarkeit - Nachmittag', {
            'fields': ('mo_pm', 'tu_pm', 'we_pm', 'th_pm', 'fr_pm')
        }),
        ('Anzeige-Informationen', {
            'fields': ('classes_cli', 'levels_cli', 'subjects_cli', 'summary'),
            'classes': ('collapse',)
        }),
        ('System', {
            'fields': ('created_timestamp', 'ref_no', 'url'),
            'classes': ('collapse',)
        }),
    )


@admin.register(SchoolClass)
class SchoolClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'level', 'year', 'school_year')
    list_filter = ('department', 'level', 'school_year')
    search_fields = ('name',)


@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'department', 'time_period', 'school_class', 'subject', 'semester')
    list_filter = ('department', 'semester', 'subject')
    search_fields = ('teacher__first_name', 'teacher__last_name', 'school_class__name')


@admin.register(SubstitutionLesson)
class SubstitutionLessonAdmin(admin.ModelAdmin):
    list_display = ('substitution', 'time_period', 'school_class', 'subject', 'candidate')
    list_filter = ('substitution__department', 'subject')
    search_fields = ('substitution__id', 'school_class__name')


@admin.register(SubstitutionCandidate)
class SubstitutionCandidateAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'substitution', 'rating', 'invited_date', 'response_date', 'response_type')
    list_filter = ('response_type', 'invited_date', 'response_date')
    search_fields = ('candidate__first_name', 'candidate__last_name')
    readonly_fields = ('record_created_date',)
    
    fieldsets = (
        ('Grundinformationen', {
            'fields': ('substitution', 'candidate', 'rating')
        }),
        ('Matching-Kriterien', {
            'fields': ('matching_half_days', 'matching_subjects', 'num_experiences', 
                      'num_experiences_in_school', 'num_experiences_with_class', 
                      'num_experiences_with_subjects')
        }),
        ('Kommunikation', {
            'fields': ('invited_date', 'response_date', 'response_type', 'comments')
        }),
        ('System', {
            'fields': ('record_created_date',),
            'classes': ('collapse',)
        }),
    )


@admin.register(SubstitutionExecution)
class SubstitutionExecutionAdmin(admin.ModelAdmin):
    list_display = ('substitution', 'candidate', 'rating', 'star_rating', 'comments')
    list_filter = ('rating',)
    search_fields = ('candidate__first_name', 'candidate__last_name', 'comments')


# ============= Vacations =============

@admin.register(Vacation)
class VacationAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_from', 'date_to', 'DayPart')
    list_filter = ('DayPart',)
    date_hierarchy = 'date_from'


@admin.register(SchoolDay)
class SchoolDayAdmin(admin.ModelAdmin):
    list_display = ('date', 'vacation', 'daypart')
    list_filter = ('vacation', 'daypart')
    date_hierarchy = 'date'


# ============= Communications =============

@admin.register(Communication)
class CommunicationAdmin(admin.ModelAdmin):
    list_display = ('request_date', 'candidate', 'substitution', 'type', 'response_type', 'response_date')
    list_filter = ('type', 'response_type', 'request_date', 'response_date')
    search_fields = ('candidate__first_name', 'candidate__last_name', 'request_text', 'response_text')
    date_hierarchy = 'request_date'
    
    fieldsets = (
        ('Grundinformationen', {
            'fields': ('substitution', 'candidate', 'type')
        }),
        ('Anfrage', {
            'fields': ('request_date', 'request_text')
        }),
        ('Antwort', {
            'fields': ('response_date', 'response_type', 'response_text')
        }),
        ('Bemerkungen', {
            'fields': ('comments',)
        }),
    )


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('request_date', 'candidate', 'substitution', 'response_type', 'response_date')
    list_filter = ('response_type', 'request_date', 'response_date')
    search_fields = ('candidate__first_name', 'candidate__last_name')
    date_hierarchy = 'request_date'


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ('request_date', 'candidate', 'substitution', 'response_type', 'response_date')
    list_filter = ('response_type', 'request_date', 'response_date')
    search_fields = ('candidate__first_name', 'candidate__last_name')
    date_hierarchy = 'request_date'
    readonly_fields = ('response_to_invitation_url',)


# Customize admin site header
admin.site.site_header = "Schulverwaltung Administration"
admin.site.site_title = "Schulverwaltung Admin"
admin.site.index_title = "Willkommen zur Schulverwaltung"
