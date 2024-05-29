from django.forms import modelformset_factory
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import DetailView, UpdateView, CreateView
from .models import School, Person, Substitution, SubstitutionPeriod, Lesson, Location, Level
from .forms import SchoolForm, CandidateForm, SubstitutionForm, TeacherForm, SubstitutionPeriodForm
from django.views.generic import ListView  # Import the necessary module
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
# from django.views.generic.edit import CreateView

class SchoolListView(ListView):
    model = School
    context_object_name = "schools"  # The name of the variable to be used in the template
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
        context['locations'] = Location.objects.all()  # Pass all locations to the template
        context['levels'] = Level.objects.all()  # Pass all locations to the template
        return context


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
            queryset = queryset.filter(last_name__icontains=name_filter)
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


class SubstitutionCreateView(CreateView):
    model = Substitution
    form_class = SubstitutionForm
    template_name = "school_management/substitution_create.html"
    success_url = reverse_lazy("substitution_list")

    def form_valid(self, form):
        self.object = form.save()
        self.object.create_substitution_items()  # Call the method after saving the form
        return redirect('substitution_edit', pk=self.object.pk)
    
    
class SubstitutionEditView(UpdateView):
    model = Substitution
    form_class = SubstitutionForm
    template_name = "school_management/substitution_edit.html"
    success_url = reverse_lazy("substitution_list")

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        if pk:
            return get_object_or_404(Substitution, pk=pk)
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        substitution = self.get_object()
        SubstitutionPeriodFormSet = modelformset_factory(SubstitutionPeriod, form=SubstitutionPeriodForm, extra=0)
        if self.request.POST:
            formset = SubstitutionPeriodFormSet(self.request.POST, queryset=SubstitutionPeriod.objects.filter(substitution=substitution))
        else:
            formset = SubstitutionPeriodFormSet(queryset=SubstitutionPeriod.objects.filter(substitution=substitution))
        context['formset'] = formset
        return context

    def post(self, request, *args, **kwargs):
        print(f'KWARGS: {kwargs}')  # Debugging line
        form = self.get_form()
        self.object = self.get_object()
        print(f'Object: {self.object}')  # Debugging line
        SubstitutionPeriodFormSet = modelformset_factory(SubstitutionPeriod, form=SubstitutionPeriodForm, extra=0)
        formset = SubstitutionPeriodFormSet(self.request.POST, queryset=SubstitutionPeriod.objects.filter(substitution=self.object))
        
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            try:
                self.object.create_substitution_items()
            except AttributeError as e:
                print(f'Error: {e}')
                return self.form_invalid(form, formset, error=str(e))
            formset.save()
            return self.form_valid(form, formset)
        else:
            print('Form or formset invalid')
            return self.form_invalid(form, formset)

    def form_valid(self, form, formset):
        form.save()
        formset.save()
        return redirect(self.success_url)

    def form_invalid(self, form, formset, error=None):
        context = self.get_context_data(form=form, formset=formset)
        if error:
            context['error'] = error
        return self.render_to_response(context)
