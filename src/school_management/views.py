from django.forms import modelformset_factory
from django.http import HttpResponse
from django.views import View
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, UpdateView, CreateView, DeleteView
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from collections import Counter
from django.db.models import Value, CharField
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from .texte import texte
from twilio.rest import Client

from .models import (
    School,
    Person,
    Teacher,
    Candidate,
    Substitution,
    Subject,
    Timetable,
    Location,
    Level,
    SubstitutionStatus,
    SubstitutionCandidate,
    Invitation,
    Application,
    CommunicationType,
    CommunicationTypeEnum,
    Communication,
    CommunicationResponseType,
    CommunicationResponseTypeEnum,
)
from .forms import (
    SchoolForm,
    CandidateForm,
    SubstitutionCreateForm,
    SubstitutionEditForm,
    TeacherForm,
    InvitationForm,
    ApplicationForm,
    ApplicationRequestForm,
    ResponseForm,
    # ApplicationFullForm,
    ApplicationResponseForm
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
        context["locations"] = (
            Location.objects.all()
        )  # Pass all locations to the template
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
        # context["school_teachers"] = school.school_persons.filter(is_teacher=True)
        context["school_classes"] = school.class_schools.filter(school=school)
        context["substitutions"] = school.substitution_schools.filter(school=school)
        lessons = Timetable.objects.filter(school=school)
        teachers = [l.teacher for l in lessons]
        context["teachers"] = list(set(teachers))
        return context


class SchoolEditView(LoginRequiredMixin, UpdateView):
    model = School
    form_class = SchoolForm
    template_name = "school_management/school_edit.html"
    success_url = reverse_lazy(
        "school_list"
    )


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
        year_filter = self.request.GET.get("year_filter", "")

        # Apply filters if present
        if first_name_filter:
            queryset = queryset.filter(first_name__icontains=first_name_filter)
        if last_name_filter:
            queryset = queryset.filter(last_name__icontains=last_name_filter)
        if year_filter:
            queryset = queryset.filter(year_of_birth__icontains=year_filter)

        return queryset


class CandidateDetailView(DetailView):
    model = Candidate
    template_name = "school_management/candidate_detail.html"
    context_object_name = "candidate"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        candidate = context["candidate"]
        all_subjects = []
        for substitution_candidate in SubstitutionCandidate.objects.filter(
            candidate=candidate, selected_date__isnull=False
        ):
            h = SubstitutionHelper(substitution_candidate.substitution)
            all_subjects += h.subjects
        context["taught_subjects"] = dict(Counter([x.name for x in all_subjects]))
        context["dateidates"] = dict(Counter([x.name for x in all_subjects]))
        return context


class CandidateEditView(LoginRequiredMixin, UpdateView):
    model = Candidate
    form_class = CandidateForm
    template_name = "school_management/candidate_edit.html"
    success_url = reverse_lazy("school_management:candidate_list")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        action = request.POST.get("action")
        if form.is_valid():
            if action == "save":
                self.object = form.save(commit=False)
                self.object.save()
                return self.form_valid(form)
            elif action == "delete":
                self.object.delete()
                messages.success(request, "Das Profil wurde erfolgreich gelöscht.")
                return redirect(self.success_url)
        else:
            print("Form invalid")
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add the candidate object to the context
        context["candidate"] = self.object
        return context

    def form_valid(self, form):
        form.save()
        return redirect(self.success_url)

    def form_invalid(self, form, error=None):
        context = self.get_context_data(form=form)
        if error:
            context["error"] = error
        return self.render_to_response(context)


class TeacherListView(ListView):
    model = Timetable
    template_name = "school_management/teacher_list.html"  # Path to the template
    context_object_name = "teachers"

    def get_queryset(self):
        # Get unique combinations of teacher and school from the Timetable model
        queryset = (
            Timetable.objects.select_related("teacher", "school")
            .values(
                "teacher__id",
                "teacher__first_name",
                "teacher__last_name",
                "teacher__phone_number",
                "teacher__email",
                "school__name",
            )
            .distinct()
        )
        name_filter = self.request.GET.get("name_filter", "")

        # Apply filters if present
        if name_filter:
            queryset = queryset.filter(
                teacher__person__last_name__icontains=name_filter
            )

        # Order by teacher's last name
        queryset = queryset.order_by("teacher__last_name")

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
        context["schools"] = list(
            Timetable.objects.filter(teacher=teacher)
            .values_list("school__name", flat=True)
            .distinct()
        )
        context["subjects"] = teacher.get_unique_subjects()
        context["classes"] = teacher.get_unique_classes()
        day_list = teacher.get_unique_days()
        context["days"] = f"{len(day_list)}, ({', '.join(day_list)})"
        return context


class TeacherEditView(LoginRequiredMixin, UpdateView):
    model = Teacher
    form_class = TeacherForm
    template_name = "school_management/teacher_edit.html"
    success_url = reverse_lazy("school_management:teacher_list")


class SubstitutionCandidatesListView(ListView):
    model = Substitution
    context_object_name = "substitutions"
    template_name = (
        "school_management/substitution_candidates_list.html"  # Path to the template
    )
    success_url = reverse_lazy("school_management/substitution_candidates_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["status"] = SubstitutionStatus.objects.all()

        context["schools"] = School.objects.all().order_by("name")
        context["subjects"] = Subject.objects.all().order_by("name")
        context["levels"] = Level.objects.all().order_by("order")
        return context

    def post(self, request, *args, **kwargs):
        form = SubstitutionEditForm(request.POST)
        action = request.POST.get("action")
        if action == "send_email":
            id = request.POST.get("substitution_id")
            substitution = Substitution.objects.get(pk=id)
            helper = SubstitutionHelper(substitution)
            subject = f"Bewerbung für Vertretung {id}"
            message = f"This is a test email body for substitution {id} sent by {self.request.user.username}"
            helper.send_email(subject, message)
        return redirect(self.success_url)

    def get_queryset(self):
        queryset = super().get_queryset()
        school_filter = self.request.GET.get("school_filter", "")
        level_filter = self.request.GET.get("level_filter", "")
        date_from_filter = self.request.GET.get("date_from_filter", "")
        date_to_filter = self.request.GET.get("date_to_filter", "")
        status_filter = self.request.GET.get("status_filter", "")
        subject_filter = self.request.GET.get("subject_filter", "")
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
        queryset = queryset.filter(status_id=1, end_date__gt=yesterday)
        if school_filter:
            queryset = queryset.filter(school_id=school_filter)
        if level_filter:
            queryset = queryset.filter(levels__icontains=level_filter)
        if date_from_filter:
            queryset = queryset.filter(start_date__gt=date_from_filter)
        if date_to_filter:
            queryset = queryset.filter(end_date__lt=date_to_filter)
        if subject_filter:
            queryset = queryset.filter(subjects__icontains=subject_filter)

        queryset = queryset.order_by("start_date")
        return queryset


class SubstitutionAdminListView(ListView):
    model = Substitution
    context_object_name = (
        "substitutions"  # The name of the variable to be used in the template
    )
    template_name = (
        "school_management/substitution_admin_list.html"  # Path to the template
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["status"] = (
            SubstitutionStatus.objects.all()
        )  # Pass all locations to the template
        context["schools"] = School.objects.all()  # Pass all locations to the template
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        id_filter = self.request.GET.get("id_filter", "")
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
        if id_filter:
            queryset = queryset.filter(pk=id_filter)
        if school_filter:
            queryset = queryset.filter(school_id=school_filter)
        if teacher_filter:
            queryset = queryset.filter(
                Q(teacher__last_name__icontains=teacher_filter)
                | Q(teacher__first_name__icontains=teacher_filter)
            )
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

        queryset = queryset.order_by("start_date").order_by("-id")
        return queryset


class SubstitutionDetailView(DetailView):
    model = Substitution
    template_name = "school_management/substitution_detail.html"
    context_object_name = "substitution"

    def get_context_data(self, **kwargs):
        substitution = self.get_object()
        substitution_helper = SubstitutionHelper(substitution)
        context = super().get_context_data(**kwargs)
        context["completed_by"] = SubstitutionCandidate.objects.filter(
            substitution=substitution, selected_date__isnull=False
        ).order_by("selected_date")
        context["timetable"] = substitution_helper.lessons
        context["candidates"] = SubstitutionCandidate.objects.filter(
            substitution=substitution
        ).order_by("-rating")
        context["halfdays"] = substitution_helper.get_half_days()
        context["applications"] = Application.objects.filter(substitution=substitution)
        context["confirmed"] = Application.objects.filter(substitution=substitution, response_type_id=CommunicationResponseTypeEnum.ZUSAGE.value)
        return context


class SubstitutionCreateView(CreateView):
    model = Substitution
    form_class = SubstitutionCreateForm
    template_name = "school_management/substitution_create.html"

    def form_valid(self, form):
        self.object = form.save()
        helper = SubstitutionHelper(self.object)
        helper.assign_values()
        self.object.save()
        return redirect(
            reverse(
                "school_management:substitution_detail", kwargs={"pk": self.object.pk}
            )
        )


class SubstitutionCreateWithTeacherView(CreateView):
    model = Substitution
    form_class = SubstitutionCreateForm
    template_name = "school_management/substitution_create.html"

    def get_initial(self):
        initial = super().get_initial()
        teacher_id = self.kwargs.get("teacher_id")
        if teacher_id:
            teacher = get_object_or_404(Teacher, id=teacher_id)
            school = teacher.get_school()
            initial["teacher"] = teacher
            initial["school"] = school
        return initial

    def form_valid(self, form):
        self.object = form.save()
        helper = SubstitutionHelper(self.object)
        helper.assign_values()
        self.object.save()
        return redirect(
            reverse(
                "school_management:substitution_detail", kwargs={"pk": self.object.pk}
            )
        )


class SubstitutionEditView(UpdateView):
    model = Substitution
    form_class = SubstitutionEditForm
    template_name = "school_management/substitution_edit.html"

    def get_object(self, queryset=None):
        pk = self.kwargs.get("pk")
        if pk:
            return get_object_or_404(Substitution, pk=pk)
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        substitution = self.get_object()
        context["applications"] = Application.objects.filter(substitution=substitution)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        action = request.POST.get("action")

        if form.is_valid():
            if action == "save":
                self.object = form.save(commit=False)
                helper = SubstitutionHelper(self.object)
                helper.assign_values()

                self.object.save()
                return self.form_valid(form)
            elif action == "delete":
                self.object.delete()
                messages.success(
                    request, "Die Stellvertretung wurde erfolgreich gelöscht."
                )
                return redirect(self.get_success_url())  # Use method call here
        else:
            print("Form invalid")
            return self.form_invalid(form)

    def get_success_url(self):
        if self.object:
            return reverse(
                "school_management:substitution_detail", kwargs={"pk": self.object.pk}
            )
        else:
            # Handle the case where the object is None
            return reverse("school_management:substitution_list")  # Or any fallback URL

    def form_valid(self, form):
        form.save()
        return redirect(self.get_success_url())  # Use method call here

    def form_invalid(self, form, error=None):
        context = self.get_context_data(form=form)
        if error:
            context["error"] = error
        return self.render_to_response(context)


class ApplicationCreateView(View):

    def post(self, request, *args, **kwargs):
        form = ApplicationForm(request.POST)
        if form.is_valid():
            substitution_id = request.POST.getlist("substitution")[0] 
            substitution = get_object_or_404(Substitution, id=substitution_id)
            candidate = get_object_or_404(Person, user=request.user)
            application_type = get_object_or_404(CommunicationType, id=1)

            # Create the Application instance
            application = Application(
                substitution=substitution,
                response_type = CommunicationResponseType.objects.get(pk=4),
                candidate=candidate,
                type=application_type,
                request_date=timezone.now(),
                request_text=form.cleaned_data["request_text"],
            )
            application.save()

            # Determine the action and perform the corresponding task
            action = request.POST.get("action")
            if action == "apply":
                # Send email logic here
                subject = f"Bewerbung für Vertretung {substitution_id} ({application.substitution.school.name}, {application.substitution.start_date} - {application.substitution.end_date}, Vertretung von {application.substitution.teacher.fullname})"
                message = application.request_text
                message += f'<br><br><a href="{settings.BASE_URL}/school_management/candidates/{candidate.id}/">{candidate.fullname}</a>'
                message += f'Link: <a href="{settings.BASE_URL}/school_management/application/{application.id}/edit/">Bewerbung bearbeiten</a>'
                helper = SubstitutionHelper(substitution)
                helper.send_email(subject, message)

                messages.success(request, "Ihre Bewerbung wurde erfolgreich abgeschickt.")
                success_url = reverse("school_management:substitution_candidates_list")
            else:
                success_url = reverse(
                    "school_management:application_create", kwargs={"id": substitution_id}
                )

            return redirect(success_url)
        else:
            messages.error(request, "Das Formular enthält Fehler.")
            return redirect(reverse("school_management:application_create"))
        

    def get(self, request, *args, **kwargs):
        candidate = get_object_or_404(Person, user=request.user)
        

        substitution_id = kwargs.get("id")
        substitution = get_object_or_404(
            Substitution, id=substitution_id
        )  # Ensure substitution is fetched here
        initial_data = {
            "substitution": substitution,
            "candidate": candidate,
            "request_text": "Hier können Sie Ihre Nachricht eingeben...",
        }
        form = ApplicationRequestForm(initial=initial_data)
        context = {
            "form": form,
            "substitution": substitution,
            "candidate": candidate,
            "username": request.user.username,
            "substitution_id": substitution_id,
        }
        return render(request, "school_management/application_create.html", context)


class ApplicationResponseView(View):
    def post(self, request, *args, **kwargs):
        print(2143)
        application_id = request.POST.get("application_id")
        success_url = reverse(
            "school_management:application_edit", kwargs={"id": application_id}
        )
        application = get_object_or_404(Application, id=application_id)

        if not application.response_date:
            print("Response date not set")
            
            application.response_text = request.POST.get("response_text", "")
            application_type = get_object_or_404(CommunicationType, id=1)
        
        # Determine the action and perform the corresponding task
        action = request.POST.get("action")
        print(12354)
        if action == "send_mail":
            # Send email logic here
            subject = f"Ihre Bewerbung für Vertretung {application_id} ({application.substitution.school.name}, {application.substitution.start_date} - {application.substitution.end_date}, Vertrung von {application.substitution.teacher.fullname})"
            helper = SubstitutionHelper(application.substitution)
            application.response_text = request.POST.get("response_text")
            application.response_date = timezone.now()
            application.response_type = request.POST.get("response_type")
            application.author = get_object_or_404(Person, user=request.user)
            print(application.response_text)
            if helper.send_email(subject, application.response_text):
                messages.success(request, "Ihre Bewerbung wurde erfolgreich abgeschickt.")
                application.save()
                success_url = reverse("school_management:substitution_candidates_list")
            else:
                messages.error(request, "Beim Versenden der Email ist ein Fehler aufgetreten.")

        if action == "save":
            application.save()
            success_url = reverse("school_management:substitution_candidates_list")

        return redirect(success_url)

    def get(self, request, *args, **kwargs):
        form = ResponseForm()
        application = get_object_or_404(
            Application, id=kwargs.get("id")
        )
        author = get_object_or_404(Person, user=request.user)
        context = {
            "form": form,
            "application": application,
            "username": request.user.username,
            "author": author.fullname,
        }
        return render(request, "school_management/application_edit.html", context)


class InvitationCreateView(LoginRequiredMixin, CreateView):
    model = Invitation
    form_class = InvitationForm
    template_name = "school_management/invitation_create.html"
    success_url = reverse_lazy(
        "school_list"
    )  # Redirect to school list view after saving


def admin_tasks(request):
    return render(request, "school_management/admin_tasks.html")


def calculate_teacher_availability(request):
    # Fetch all teachers and their schedules
    teachers = Teacher.objects.all()
    schedules = Timetable.objects.filter(teacher__in=teachers)

    # Example calculation logic
    availability = {}
    for teacher in teachers:
        teacher.availability_mo_am = schedules.filter(
            teacher=teacher, day_id=1, period__time_of_day__id=0
        ).exists()
        teacher.availability_mo_pm = schedules.filter(
            teacher=teacher, day_id=1, period__time_of_day__id=1
        ).exists()
        teacher.availability_th_am = schedules.filter(
            teacher=teacher, day_id=4, period__time_of_day__id=0
        ).exists()
        teacher.availability_th_pm = schedules.filter(
            teacher=teacher, day_id=4, period__time_of_day__id=1
        ).exists()
        teacher.availability_tu_am = schedules.filter(
            teacher=teacher, day_id=2, period__time_of_day__id=0
        ).exists()
        teacher.availability_tu_pm = schedules.filter(
            teacher=teacher, day_id=2, period__time_of_day__id=1
        ).exists()
        teacher.availability_we_am = schedules.filter(
            teacher=teacher, day_id=3, period__time_of_day__id=0
        ).exists()
        teacher.availability_we_pm = schedules.filter(
            teacher=teacher, day_id=3, period__time_of_day__id=1
        ).exists()
        teacher.availability_fr_am = schedules.filter(
            teacher=teacher, day_id=5, period__time_of_day__id=0
        ).exists()
        teacher.availability_fr_pm = schedules.filter(
            teacher=teacher, day_id=5, period__time_of_day__id=1
        ).exists()
        teacher.save()

    messages.success(request, "Die Verfügbarkeit der Lehrer wurde aktualisiert")
    return redirect("school_management:admin_tasks")


class ApplicationListView(ListView):
    model = Application
    context_object_name = "applications"
    template_name = "school_management/applications_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        application_filter = self.request.GET.get("application_filter", "")
        substitution_filter = self.request.GET.get("substitution_filter", "")
        candidate_filter = self.request.GET.get("candidate_filter", "")
        substitution_date_filter_from = self.request.GET.get(
            "substitution_date_filter_from", ""
        )
        substitution_date_filter_to = self.request.GET.get(
            "substitution_date_filter_to", ""
        )
        response_filter = self.request.GET.get("response_filter", "")

        if substitution_filter:
            queryset = queryset.filter(substitution_id=substitution_filter)
        if application_filter:
            queryset = queryset.filter(id=application_filter)
        if candidate_filter:
            queryset = queryset.filter(
                Q(candidate__first_name__icontains=candidate_filter)
                | Q(candidate__last_name__icontains=candidate_filter)
            )
        if substitution_date_filter_from:
            queryset = queryset.filter(
                substitution__start_date__gte=substitution_date_filter_from
            )
        if substitution_date_filter_to:
            queryset = queryset.filter(
                substitution__start_date__lte=substitution_date_filter_to
            )
        if response_filter:
            queryset = queryset.filter(response_type_id=response_filter)

        queryset = queryset.order_by("-request_date")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add response codes to the context
        context["responses"] = CommunicationResponseType.objects.all()
        return context


class ApplicationDetailView(DetailView):
    model = Application
    template_name = "school_management/application_detail.html"
    context_object_name = "application"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ApplicationEditView(LoginRequiredMixin, UpdateView):
    model = Application
    form_class = ApplicationResponseForm
    template_name = "school_management/application_edit.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        application = self.object
        school = application.substitution.school
        # Define the 'antworten' dictionary
        context["antworten"] = {
            "bestaetigung": texte['antwort_bewerbung']['bestaetigung'],
            "absage": texte['antwort_bewerbung']['absage'],
            "annahme": texte['antwort_bewerbung']['annahme'].format(school.phone_number, school.email),
        }

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  # Retrieve the existing object
        form = self.get_form()
        action = request.POST.get("action")  # Determine the action from the form

        if form.is_valid():
            application = form.save(commit=False)  # Get the object without saving to the DB
            print(application.response_text)
            # Handle manual updates if needed (e.g., response_date, response_type)
            if action == "send":
                application.response_date = timezone.now() 
                if application.candidate.send_email:
                    self.send_email(application)
                if application.candidate.send_sms:
                    self.send_sms(application)

            # Save the updated object to the database
            application.save()

            # Redirect to the success URL
            return redirect(self.get_success_url())
        else:
            # If the form is invalid, return the form with errors
            return self.form_invalid(form)

    def send_sms(self, application):
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_ACCOUNT_TOKEN)
        body = (
            f"{application.subject()}\n"
            f"{application.response_text}\n"
            "Weitere Informationen unter:\n"
            f"{settings.BASE_URL}{reverse('school_management:application_detail', kwargs={'pk': application.id})}\n"
        ).strip()
        message = client.messages.create(
            body=body,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=application.candidate.phone_number,
        )

        print(f"Message sent with SID: {message.sid}")
        messages.success(self.request, "Deine Email wurde erfolgreich versandt.")

    def send_email(self, application):
        subject = "Betreff"  # Set your subject here
        message = application.response_text
        recipient = application.candidate.email

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [recipient],
            fail_silently=False,
        )
        messages.success(self.request, "Deine SMS wurde erfolgreich versandt.")

    
    def get_success_url(self):
        return reverse("school_management:application_list")


class CandidateCreateView(CreateView):
    model = Person
    fields = [
        "first_name",
        "last_name",
        "email",
        "phone_number",
        "subjects",
        "is_candidate",
    ]
    template_name = "school_management/candidate_form.html"
    success_url = reverse_lazy(
        "school_management:candidate_list"
    )  # Redirect to a list of candidates or another view after creation

    def form_valid(self, form):
        # Ensure that the person is marked as a candidate
        form.instance.is_candidate = True
        return super().form_valid(form)


class CandidateDeleteView(DeleteView):
    model = Person
    template_name = "school_management/candidate_confirm_delete.html"
    success_url = reverse_lazy(
        "school_management:candidate_list"
    )  # Redirect to a list of candidates after deletion

    def get_queryset(self):
        # Ensure that only candidates can be deleted via this view
        return super().get_queryset().filter(is_candidate=True)


def invite_candidates(request, id):
    selected_candidate = get_object_or_404(SubstitutionCandidate, id=id)
    author = get_object_or_404(Person, user=request.user)
    # Check if an invitation already exists for this candidate and substitution
    invitation, created = Communication.objects.get_or_create(
        type=CommunicationType.objects.get(pk=CommunicationTypeEnum.EINLADUNG.value),
        candidate=selected_candidate.candidate,
        substitution=selected_candidate.substitution,
        defaults={
            "request_date": timezone.now(),
            "request_text": texte["default_invitiation_email"].format(
                selected_candidate.candidate.informal_salutation,
                selected_candidate.substitution.school.name,
                selected_candidate.substitution.url(),
                selected_candidate.substitution.school.email,
                selected_candidate.substitution.school.phone_number,
                author.first_last_name,
            ),
        },
    )

    # If it's a POST request, process the submitted form data
    if request.method == "POST":
        form = InvitationForm(request.POST, instance=invitation)
        if form.is_valid():
            form.save()  # Save the form data (updates the invitation if necessary)
            return render(request, "success.html")  # Redirect to a success page
    else:
        # Prepopulate the form with the invitation instance
        form = InvitationForm(instance=invitation)

    context = {
        "substitution": selected_candidate.substitution,
        "candidate": selected_candidate.candidate,
        "form": form,
    }
    return render(request, "school_management/invite_candidates.html", context)
