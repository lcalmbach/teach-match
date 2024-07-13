from django import forms
from .models import School, Person, Substitution, Teacher, Candidate, Invitation, Application
import fitz  # PyMuPDF


class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = "__all__"

class InvitationForm(forms.ModelForm):
    class Meta:
        model = Invitation
        fields = "__all__"

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['request_text']  # Include other fields if necessary
        labels = {
            'answer_text': 'Bemerkungen zur Bewerbung',
        }
        widgets = {
            'request_text': forms.Textarea(attrs={'rows': 4}),
            'substitution': forms.HiddenInput(),
            'candidate': forms.HiddenInput(),
        }

class ResponseForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['answer_text']  # Include other fields if necessary
        labels = {
            'answer_text': 'Antwort',
        }
        widgets = {
            'answer_text': forms.Textarea(attrs={'rows': 8}),
        }



class CandidateForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "available_from_date",
            "available_to_date",
            "availability_mo_am",
            "availability_mo_pm",
            "availability_tu_am",
            "availability_tu_pm",
            "availability_we_am",
            "availability_we_pm",
            "availability_th_am",
            "availability_th_pm",
            "availability_fr_am",
            "availability_fr_pm",
            "availability_comment",
        ]

    def save(self, commit=True):
        # Call the parent class's save method to get the model instance
        instance = super(CandidateForm, self).save(commit=False)

        # Check if a new file was uploaded
        # if self.cleaned_data["cv_file"]:
        #    pdf_file = self.cleaned_data["cv_file"]
        #    # Extract text from PDF
        #    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
        #    text = ""
        #    for page in doc:
        #        text += page.get_text()
        #    doc.close()
        #
        #    # Assign the extracted text to the cv_text field
        #    instance.cv_text = text

        if commit:
            instance.save()
            self.save_m2m()  # In case there are many-to-many fields
        return instance


class SubstitutionForm(forms.ModelForm):
    class Meta:
        model = Substitution
        exclude =  [
            "mo_am",
            "mo_pm",
            "tu_am",
            "tu_pm",
            "we_am",
            "we_pm",
            "th_am",
            "th_pm",
            "fr_am",
            "fr_pm",
            "classes",
            "levels",
            "subjects",
        ]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}, format='%Y-%m-%d'),
            "end_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}, format='%Y-%m-%d'),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_date'].input_formats = ['%Y-%m-%d']
        self.fields['end_date'].input_formats = ['%Y-%m-%d']



class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = [
            "first_name",
            "last_name",
            "initials",
            "email",
            "phone_number",
        ]
