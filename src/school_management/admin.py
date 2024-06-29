from django.contrib import admin

from .models import (
    SubstitutionCause,
    SchoolPersonRole,
    Location,
    Gender,
    Certificate,
    TimeOfDay,
    DayOfWeek,
    Period,
    Level,
    Subject,
    School,
    Person,
    Candidate,
    SchoolClass,
    Timetable,
    Vacation,
    Substitution,
    SubstitutionCandidate,
)

# ist ein Versuch, die Admin-Oberfläche zu verbessern, im Moment erscheint der description Text aber noch nicht. Das scheint
# komplizierter zu sein, man muss im templates folder ein eigenes template vorgeben, ev. machen wir das für die produktive Version
# aber noch nicht für den POC
class SchoolAdmin(admin.ModelAdmin):
    model = School
    # Custom fieldsets to include model-level help text
    fieldsets = (
        (
            None,
            {
                "fields": ("name", "level", "address", "url", "location", "plz"),
                "description": "Schulstandort mit Adresse und URL",
            },
        ),
    )


admin.site.register(SubstitutionCause)
admin.site.register(SchoolPersonRole)
admin.site.register(Location)
admin.site.register(Gender)
admin.site.register(Certificate)
admin.site.register(TimeOfDay)
admin.site.register(DayOfWeek)
admin.site.register(Period)
admin.site.register(Level)
admin.site.register(Subject)
admin.site.register(School, SchoolAdmin)
admin.site.register(Candidate)
admin.site.register(SchoolClass)
admin.site.register(Timetable)
admin.site.register(Vacation)
admin.site.register(Substitution)
admin.site.register(SubstitutionCandidate)
