from django.forms import modelformset_factory
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import DetailView, UpdateView, CreateView
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta

from .models import (
    School,
    Person,
    Teacher,
    Candidate,
    Substitution,
    Timetable,
    Location,
    Level,
    SubstitutionStatus,
    SubstitutionCandidate,
)
from .forms import (
    SchoolForm,
    CandidateForm,
    SubstitutionForm,
    TeacherForm,
)
from django.views.generic import ListView  # Import the necessary module
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.db.models.functions import Concat
from django.db.models import F, Value

from .helpers import SubstitutionHelper

# from django.views.generic.edit import CreateView


class SchoolListView(ListView):
    model = School
    context_object_name = (
        "schools"  # The name of the variable to be used in the template
    )
    template_name = "school_management/school_list.html"  # Path to the template

    def get_queryset(self):
        queryset = super().get_queryset()  # Get the original queryset
        name_filter = self.request.GET.get("name_filter", "")
        level_filter = self.request.GET.get("level_filter", "")
        location_filter = self.request.GET.get("location_filter", "")

        # Apply filters if present
        if name_filter:
            queryset = queryset.filter(name__icontains=name_filter)
        if level_filter:
            queryset = queryset.filter(level__id=level_filter)
        if location_filter:
            queryset = queryset.filter(location__id=location_filter)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[
            "locations"
        ] = Location.objects.all()  # Pass all locations to the template
        context["levels"] = Level.objects.all()  # Pass all locations to the template
        return context


class SchoolDetailView(DetailView):
    model = School
    template_name = "school_management/school_detail.html"
    context_object_name = "school"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school = context["school"]
        # Filter SchoolPerson by school and role ID
        context["school_contacts"] = school.school_person_schools.filter(role__id=1)
        context["school_teachers"] = school.school_person_schools.filter(role__id=4)
        context["school_classes"] = school.class_schools.filter(school=school)
        context["substitutions"] = school.substitution_schools.filter(school=school)

        return context


class SchoolEditView(LoginRequiredMixin, UpdateView):
    model = School
    form_class = SchoolForm
    template_name = "school_management/school_edit.html"
    success_url = reverse_lazy(
        "school_list"
    )  # Redirect to school list view after saving


class CandidateListView(ListView):
    model = Candidate
    context_object_name = (
        "candidates"  # The name of the variable to be used in the template
    )
    template_name = "school_management/candidate_list.html"  # Path to the template

    def get_queryset(self):
        queryset = super().get_queryset()  # Get the original queryset
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
    model = Candidate
    template_name = "school_management/candidate_detail.html"
    context_object_name = "candidate"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        candidate = context["candidate"]
        context["availabilities"] = candidate.availability_templates_candidate.all()
        context["subjects"] = candidate.personsubject_persons.all()
        context["certificates"] = candidate.certificates.all()
        context["substitutions"] = candidate.substitution_deputies.all()

        return context


class CandidateEditView(LoginRequiredMixin, UpdateView):
    model = Candidate
    form_class = CandidateForm
    template_name = "school_management/candidate_edit.html"
    success_url = reverse_lazy("candidate_list")


class TeacherListView(ListView):
    model = Teacher
    template_name = "school_management/teacher_list.html"  # Path to the template
    context_object_name = "teachers"

    def get_queryset(self):
        queryset = (
            super()
            .get_queryset()
            .filter(role__id=4)
            .annotate(
                teacher=Concat(
                    F("person__first_name"), Value(" "), F("person__last_name")
                )
            )
        )
        name_filter = self.request.GET.get("name_filter", "")
        email_filter = self.request.GET.get("email_filter", "")
        phone_filter = self.request.GET.get("phone_filter", "")
        school_filter = self.request.GET.get("school_filter", "")

        # Apply filters if present
        if name_filter:
            queryset = queryset.filter(person__last_name__icontains=name_filter)
        if email_filter:
            queryset = queryset.filter(person__email__icontains=email_filter)
        if phone_filter:
            queryset = queryset.filter(person__phone_number__icontains=phone_filter)
        if school_filter:
            queryset = queryset.filter(school__name__icontains=school_filter)

        queryset = queryset.order_by("school__name", "teacher")
        return queryset


class TeacherDetailView(DetailView):
    model = Teacher
    template_name = "school_management/teacher_detail.html"
    context_object_name = "teacher"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teacher = context["teacher"]
        context["lessons"] = teacher.lessons_template_teachers.all().order_by(
            "day_id", "period_id"
        )
        context["subjects"] = teacher.get_unique_subjects()
        context["classes"] = teacher.get_unique_classes()
        return context


class TeacherEditView(LoginRequiredMixin, UpdateView):
    model = Teacher
    form_class = TeacherForm
    template_name = "school_management/teacher_edit.html"
    success_url = reverse_lazy("teacher_list")


class SubstitutionCandidatesListView(ListView):
    model = Substitution
    context_object_name = (
        "substitutions"  # The name of the variable to be used in the template
    )
    template_name = "school_management/substitution_list_candidates.html"  # Path to the template
    success_url = reverse_lazy("substitution_candidates_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[
            "status"
        ] = SubstitutionStatus.objects.all()
        
        context["schools"] = School.objects.all().order_by("name")
        context[
            "levels"
        ] = Level.objects.all().order_by("order")
        context["schools"] = School.objects.all()
        return context
    
    def post(self, request, *args, **kwargs):
        form = SubstitutionForm(request.POST)
        action = request.POST.get('action')
        print(action,form.is_valid())
        if action == 'send_email':
            id = request.POST.get('substitution_id')
            substitution = Substitution.objects.get(pk=id)
            helper = SubstitutionHelper(substitution)
            subject = f'Bewerbung für Vertretung {id}'
            message = f'This is a test email body for substitution {id} sent by {self.request.user.username}'
            helper.send_email(subject, message)
        return redirect(self.success_url)

    def get_queryset(self):
        queryset = super().get_queryset()
        school_filter = self.request.GET.get("school_filter", "")
        level_filter = self.request.GET.get("level_filter", "")
        date_from_filter = self.request.GET.get("date_from_filter", "")
        date_to_filter = self.request.GET.get("date_to_filter", "")
        status_filter = self.request.GET.get("status_filter", "")
        day_filters = {
            "mo_am_filter": self.request.GET.get("mo_am_filter"),
            "tu_am_filter": self.request.GET.get("tu_am_filter"),
            "we_am_filter": self.request.GET.get("we_am_filter"),
            "th_am_filter": self.request.GET.get("th_am_filter"),
            "fr_am_filter": self.request.GET.get("fr_am_filter"),
            "mo_pm_filter": self.request.GET.get("mo_pm_filter"),
            "tu_pm_filter": self.request.GET.get("tu_pm_filter"),
            "we_pm_filter": self.request.GET.get("we_pm_filter"),
            "th_pm_filter": self.request.GET.get("th_pm_filter"),
            "fr_pm_filter": self.request.GET.get("fr_pm_filter"),
        }

        # Apply filters if present
        yesterday = timezone.now() - timedelta(days=1)
        queryset = queryset.filter(status_id=3, end_date__gt=yesterday)
        if school_filter:
            queryset = queryset.filter(school_id=school_filter)
        if level_filter:
            queryset = queryset.filter(levels__icontains=level_filter)
        if date_from_filter:
            queryset = queryset.filter(start_date__gt=date_from_filter)
        if date_to_filter:
            queryset = queryset.filter(end_date__lt=date_to_filter)
        if status_filter:
            queryset = queryset.filter(status_id=status_filter)
        for key, value in day_filters.items():
            if value == "1":
                field_name = key.replace("_filter", "")
                queryset = queryset.filter(**{field_name: True})

        queryset = queryset.order_by("-start_date")
        return queryset


class SubstitutionAdminListView(ListView):
    model = Substitution
    context_object_name = (
        "substitutions"  # The name of the variable to be used in the template
    )
    template_name = "school_management/substitution_list_admin.html"  # Path to the template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[
            "status"
        ] = SubstitutionStatus.objects.all()  # Pass all locations to the template
        context["schools"] = School.objects.all()  # Pass all locations to the template
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        school_filter = self.request.GET.get("school_filter", "")
        teacher_filter = self.request.GET.get("teacher_filter", "")
        date_from_filter = self.request.GET.get("date_from_filter", "")
        date_to_filter = self.request.GET.get("date_to_filter", "")
        status_filter = self.request.GET.get("status_filter", "")
        day_filters = {
            "mo_am_filter": self.request.GET.get("mo_am_filter"),
            "tu_am_filter": self.request.GET.get("tu_am_filter"),
            "we_am_filter": self.request.GET.get("we_am_filter"),
            "th_am_filter": self.request.GET.get("th_am_filter"),
            "fr_am_filter": self.request.GET.get("fr_am_filter"),
            "mo_pm_filter": self.request.GET.get("mo_pm_filter"),
            "tu_pm_filter": self.request.GET.get("tu_pm_filter"),
            "we_pm_filter": self.request.GET.get("we_pm_filter"),
            "th_pm_filter": self.request.GET.get("th_pm_filter"),
            "fr_pm_filter": self.request.GET.get("fr_pm_filter"),
        }

        # Apply filters if present
        if school_filter:
            queryset = queryset.filter(school_id=school_filter)
        if teacher_filter:
            queryset = queryset.filter(teacher__name__icontains=teacher_filter)
        if date_from_filter:
            queryset = queryset.filter(start_date__gt=date_from_filter)
        if date_to_filter:
            queryset = queryset.filter(end_date__lt=date_to_filter)
        if status_filter:
            queryset = queryset.filter(status_id=status_filter)
        for key, value in day_filters.items():
            if value == "1":
                field_name = key.replace("_filter", "")
                queryset = queryset.filter(**{field_name: True})

        queryset = queryset.order_by("start_date")
        return queryset


class SubstitutionDetailView(DetailView):
    model = Substitution
    template_name = "school_management/substitution_detail.html"
    context_object_name = "substitution"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        substitution = self.get_object()
        context["candidates"] = substitution.substitution_candidates

        return context


class SubstitutionCreateView(CreateView):
    model = Substitution
    form_class = SubstitutionForm
    template_name = "school_management/substitution_create.html"
    success_url = reverse_lazy("substitution_admin_list")

    def get_initial(self):
        initial = super().get_initial()
        teacher_id = self.kwargs.get("teacher_id")
        if teacher_id:
            initial["teacher"] = teacher_id
        return initial

    def form_valid(self, form):
        self.object = form.save()
        return redirect("substitution_edit", pk=self.object.pk)


class SubstitutionEditView(UpdateView):
    model = Substitution
    form_class = SubstitutionForm
    template_name = "school_management/substitution_edit.html"
    success_url = reverse_lazy("substitution_admin_list")

    def get_object(self, queryset=None):
        pk = self.kwargs.get("pk")
        if pk:
            return get_object_or_404(Substitution, pk=pk)
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        substitution = self.get_object()
        if substitution:
            context['substitution_candidates'] = substitution.substitution_candidates.all().order_by('-rating')
        else:
            context['substitution_candidates'] = []

        # If any additional context is needed, add it here
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        action = request.POST.get('action')
        
        if form.is_valid():
            if action == 'save':
                self.object = form.save(commit=False)
                helper = SubstitutionHelper(self.object)
                helper.assign_values()

                self.object.save()
                return self.form_valid(form)
            elif action == 'delete':
                self.object.delete()
                messages.success(request, 'Substitution successfully deleted.')
                return redirect(self.success_url)
        else:
            print("Form invalid")
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return redirect(self.success_url)

    def form_invalid(self, form, error=None):
        context = self.get_context_data(form=form)
        if error:
            context["error"] = error
        return self.render_to_response(context)
