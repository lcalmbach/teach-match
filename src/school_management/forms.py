from django import forms
from .models import School, Person, Substitution, SubstitutionPeriod
import fitz  # PyMuPDF


class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = "__all__"


class CandidateForm(forms.ModelForm):
    class Meta:
        model = Person
        exclude = ["cv_text"]

    def save(self, commit=True):
        # Call the parent class's save method to get the model instance
        instance = super(CandidateForm, self).save(commit=False)

        # Check if a new file was uploaded
        if self.cleaned_data["cv_file"]:
            pdf_file = self.cleaned_data["cv_file"]
            # Extract text from PDF
            doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()

            # Assign the extracted text to the cv_text field
            instance.cv_text = text

        if commit:
            instance.save()
            self.save_m2m()  # In case there are many-to-many fields
        return instance


class SubstitutionForm(forms.ModelForm):
    class Meta:
        model = Substitution
        fields = "__all__"
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = "__all__"


class SubstitutionPeriodForm(forms.ModelForm):
    class Meta:
        model = SubstitutionPeriod
        fields = ['deputy', 'confirmed']
