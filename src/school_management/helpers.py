from django.apps import apps

class SubstitutionHelper:

    @staticmethod
    def get_classes(substitution):
        Lesson = apps.get_model('school_management', 'Lesson')
        SchoolClass = apps.get_model('school_management', 'SchoolClass')
        
        lessons = Lesson.objects.filter(
            teacher=substitution.teacher,
            date__range=(substitution.start_date, substitution.end_date)
        )
        
        school_classes = SchoolClass.objects.filter(
            id__in=lessons.values_list('school_class_id', flat=True)
        ).distinct()
        school_classes = [x.name for x in school_classes]
        return ', '.join(school_classes)

    @staticmethod
    def get_days(substitution):
        return []

    @staticmethod
    def get_subjects(substitution):
        return []

    @staticmethod
    def get_candidates(substitution):
        return []