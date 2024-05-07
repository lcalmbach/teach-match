from django.shortcuts import redirect
from django.views.generic import DetailView, UpdateView
from .models import School, Person, Substitution, SubstitutionPeriod, Lesson
from .forms import SchoolForm, CandidateForm, SubstitutionForm, TeacherForm
from django.views.generic import ListView  # Import the necessary module
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class SchoolListView(ListView):
    model = School
    context_object_name = (
        "schools"  # The name of the variable to be used in the template
    )
    template_name = "school_management/school_list.html"  # Path to the template


class SchoolDetailView(DetailView):
    model = School
    template_name = "school_management/school_detail.html"
    context_object_name = "school"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school = context['school']
        # Filter SchoolPerson by school and role ID
        context['school_contacts'] = school.school_person_schools.filter(role__id=1)
        context['school_teachers'] = school.school_person_schools.filter(role__id=4)
        context['school_classes'] = school.class_schools.filter(school=school)

        return context


class SchoolEditView(LoginRequiredMixin, UpdateView):
    model = School
    form_class = SchoolForm
    template_name = "school_management/school_edit.html"
    success_url = reverse_lazy(
        "school_list"
    )  # Redirect to school list view after saving


class CandidateListView(ListView):
    model = Person
    context_object_name = (
        "candidates"  # The name of the variable to be used in the template
    )
    template_name = "school_management/candidate_list.html"  # Path to the template

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_candidate=True)
        first_name_filter = self.request.GET.get("first_name_filter", "")
        last_name_filter = self.request.GET.get("last_name_filter", "")
        gender_filter = self.request.GET.get("gender_filter", "")
        year_filter = self.request.GET.get("year_filter", "")
        email_filter = self.request.GET.get("email_filter", "")
        phone_filter = self.request.GET.get("phone_filter", "")

        # Apply filters if present
        if first_name_filter:
            queryset = queryset.filter(first_name__icontains=first_name_filter)
        if last_name_filter:
            queryset = queryset.filter(last_name__icontains=last_name_filter)
        if gender_filter:
            queryset = queryset.filter(gender__name__icontains=gender_filter)
        if year_filter:
            queryset = queryset.filter(year_of_birth__icontains=year_filter)
        if email_filter:
            queryset = queryset.filter(email__icontains=email_filter)
        if phone_filter:
            queryset = queryset.filter(phone_number__icontains=phone_filter)

        return queryset


class CandidateDetailView(DetailView):
    model = Person
    template_name = "school_management/Candidate_detail.html"
    context_object_name = "candidate"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        candidate = context["candidate"]
        context['availabilities'] = candidate.availabilities.all()
        context['subjects'] = candidate.personsubject_persons.all()
        return context


class CandidateEditView(LoginRequiredMixin, UpdateView):
    model = Person
    form_class = CandidateForm
    template_name = "school_management/candidate_edit.html"
    success_url = reverse_lazy("candidate_list")


class TeacherListView(ListView):
    model = Person
    context_object_name = (
        "teachers"  # The name of the variable to be used in the template
    )
    template_name = "school_management/teacher_list.html"  # Path to the template

    def get_queryset(self):
        queryset = super().get_queryset()  # Get the original queryset
        name_filter = self.request.GET.get("name_filter", "")
        gender_filter = self.request.GET.get("gender_filter", "")
        year_filter = self.request.GET.get("year_filter", "")
        email_filter = self.request.GET.get("email_filter", "")
        phone_filter = self.request.GET.get("phone_filter", "")

        # Apply filters if present
        if name_filter:
            queryset = queryset.filter(name__icontains=name_filter)
        if gender_filter:
            queryset = queryset.filter(gender__name__icontains=gender_filter)
        if year_filter:
            queryset = queryset.filter(year_of_birth__icontains=year_filter)
        if email_filter:
            queryset = queryset.filter(email__icontains=email_filter)
        if phone_filter:
            queryset = queryset.filter(phone_number__icontains=phone_filter)

        return queryset


class TeacherDetailView(DetailView):
    model = Person
    template_name = "school_management/Teacher_detail.html"
    context_object_name = "teacher"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teacher = context["teacher"]
        context['teacher_subjects'] = teacher.personsubject_persons.all()
        context['lessons'] = teacher.lessons_template_teachers.all().order_by('day_id', 'period_id')
        return context


class TeacherEditView(LoginRequiredMixin, UpdateView):
    model = Person
    form_class = TeacherForm
    template_name = "school_management/teacher_edit.html"
    success_url = reverse_lazy("teacher_list")


class SubstitutionListView(ListView):
    model = Substitution
    context_object_name = (
        "substitutions"  # The name of the variable to be used in the template
    )
    template_name = "school_management/substitution_list.html"  # Path to the template

    def get_queryset(self):
        # Get the default queryset
        queryset = super().get_queryset()
        # Order queryset by start_date in descending order
        queryset = queryset.order_by('-start_date')
        return queryset

class SubstitutionDetailView(DetailView):
    model = Substitution
    template_name = "school_management/substitution_detail.html"
    context_object_name = "substitution"


class SubstitutionEditView(UpdateView):
    model = Substitution
    form_class = SubstitutionForm
    template_name = "school_management/substitution_edit.html"
    success_url = reverse_lazy("substitution_list")  # Redirect after successful creation or update

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        if pk:
            return super().get_object(queryset)
        return None  # Return None if no PK, this makes the form a creation form

    def form_valid(self, form):
        is_new = self.get_object() is None  # Check if creating a new object
        self.object = form.save()
        if is_new:
            # Create SubstitutionPeriod instances
            substitution = self.object  # Get the newly created Substitution object
            lesson_qs = substitution.teacher.lesson_teachers.filter(
                date__range=[substitution.start_date, substitution.end_date]
            )
            SubstitutionPeriod.create_substitution_periods(substitution, lesson_qs)
        return redirect(self.get_success_url())
