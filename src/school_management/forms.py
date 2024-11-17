from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Fieldset, Field, Submit
from django import forms
from .models import (
    School,
    Person,
    Substitution,
    Teacher,
    Candidate,
    Invitation,
    Application,
    Subject,
    Communication,
)
import fitz  # PyMuPDF

class StarRatingWidget(forms.RadioSelect):
    """Custom widget to render star rating."""
    template_name = 'widgets/star_rating.html'

class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = "__all__"


class ApplicationRequestForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ["request_text", "substitution", "candidate"]  # Include other fields if necessary
        labels = {
            "request_text": "Mitteilung",
        }
        widgets = {
            "request_text": forms.Textarea(attrs={"rows": 4}),
            "substitution": forms.HiddenInput(),
            "candidate": forms.HiddenInput(),
        }


class InvitationForm(forms.ModelForm):
    class Meta:
        model = Invitation
        fields = ["candidate", "request_text"]
        labels = {
            "candidate": "Kandidat*in",
            "request_text": "Einladungstext",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Disable the candidate field
        self.fields["candidate"].disabled = True


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ["request_text"]  # Include other fields if necessary
        labels = {
            "response_text": "Bemerkungen zur Bewerbung",
        }
        widgets = {
            "request_text": forms.Textarea(attrs={"rows": 4}),
            "substitution": forms.HiddenInput(),
            "candidate": forms.HiddenInput(),
            "request_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}, format="%Y-%m-%d"
            ),
        }

class ApplicationResponseForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = [
            "response_type",
            "response_text",
            "response_date",
        ]

        widgets = {
            "request_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}, format="%Y-%m-%d"
            ),
            "response_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}, format="%Y-%m-%d"
            ),
        }

        labels = {
            "request_text": "Bewerbung Text",
            "request_date": "Bewerbung gesendet am",
            "response_date": "Antwort am",
        }

class ApplicationRatingForm(forms.ModelForm):
    """
    ApplicationRatingForm is a Django ModelForm for the Application model, used to rate and comment on an application.
    Attributes:
        Meta:
            model (Application): The model that this form is associated with.
            fields (list): The fields to include in the form, which are "rating" and "comments".
            widgets (dict): Custom widgets for the form fields. The "rating" field uses a StarRatingWidget with choices for 1 to 5 stars.
            labels (dict): Custom labels for the form fields. The "rating" field is labeled "Bewertung der Stellvertretung" and the "comments" field is labeled "Bemerkungen zum Ablauf der Stellvertretung".
    """

    class Meta:
        model = Application
        fields = [
            "rating",  
            "comments",
        ]

        widgets = {
            "rating": StarRatingWidget(choices=[  # Add choices for star ratings
                (1, "★"),
                (2, "★★"),
                (3, "★★★"),
                (4, "★★★★"),
                (5, "★★★★★"),
            ]),
        }

        labels = {
            "rating": "Bewertung der Stellvertretung",
            "comments": "Bemerkungen zum Ablauf der Stellvertretung",
        }

class ApplicationFullForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = [
            "response_type",
            "response_text",
            "response_date",
            "rating",  
            "comments",
        ]

        widgets = {
            "request_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}, format="%Y-%m-%d"
            ),
            "response_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}, format="%Y-%m-%d"
            ),
            "rating": StarRatingWidget(choices=[  # Add choices for star ratings
                (1, "★"),
                (2, "★★"),
                (3, "★★★"),
                (4, "★★★★"),
                (5, "★★★★★"),
            ]),
        }

        labels = {
            "request_text": "Bewerbung Text",
            "request_date": "Bewerbung gesendet am",
            "response_date": "Antwort am",
            "rating": "Bewertung der Stellvertretung",
            "comments": "Bemerkungen zum Ablauf der Stellvertretung",
        }


class ApplicationListForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = "__all__"
        widgets = {
            "substitution_date_filter_from": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}, format="%Y-%m-%d"
            ),
            "substitution_date_filter_to": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}, format="%Y-%m-%d"
            ),
        }


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ["response_text"]  # Include other fields if necessary
        labels = {
            "response_text": "Antwort",
        }
        widgets = {
            "response_text": forms.Textarea(attrs={"rows": 8}),
        }


class CandidateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["subjects"].widget.attrs.update(size="20")

    class Meta:
        model = Person
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "send_email",
            "send_sms",
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
            "subjects",
        ]
        widgets = {
            "available_from_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}, format="%Y-%m-%d"
            ),
            "available_to_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}, format="%Y-%m-%d"
            ),
        }

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


class SubstitutionCreateForm(forms.ModelForm):
    class Meta:
        model = Substitution
        exclude = [
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
            "subjects",
            "levels",
            "summary",
            "comment_subsitution",
        ]
        widgets = {
            "start_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}, format="%Y-%m-%d"
            ),
            "end_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}, format="%Y-%m-%d"
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["start_date"].input_formats = ["%Y-%m-%d"]
        self.fields["end_date"].input_formats = ["%Y-%m-%d"]


class SubstitutionEditForm(forms.ModelForm):
    class Meta:
        model = Substitution
        exclude = [
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
            "subjects",
            "levels",
            "summary",
        ]
        widgets = {
            "start_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}, format="%Y-%m-%d"
            ),
            "end_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}, format="%Y-%m-%d"
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["start_date"].input_formats = ["%Y-%m-%d"]
        self.fields["end_date"].input_formats = ["%Y-%m-%d"]
        status = self.initial.get("status") or self.instance.status

        # Conditionally remove the substitution_comment field if status is not 'closed'
        print(status)
        if status != 2:
            print(123)
            self.fields.pop("selection_comment")


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = [
            "first_name",
            "last_name",
            "initials",
            "email",
            "phone_number",
            "gender",
            "availability_mo_am",
            "availability_tu_am",
            "availability_we_am",
            "availability_th_am",
            "availability_fr_am",
            "availability_mo_pm",
            "availability_tu_pm",
            "availability_we_pm",
            "availability_th_pm",
            "availability_fr_pm",
            "availability_comment",
            "notify_mail_flag",
            "notify_sms_flag",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-sm-2"
        self.helper.field_class = "col-sm-8"
        self.helper.form_tag = True

        # Define the layout with Row and Column for label and value
        # Define the layout with a Fieldset containing Rows for each field
        self.helper.layout = Layout(
            Fieldset(
                "Lehrkraft",  # Fieldset title
                "first_name",
                "last_name",
                "initials",
                "email",
                "phone_number",
                "gender",
                "notify_mail_flag",
                "notify_sms_flag",
            ),
            Fieldset(
                "Verfügbarkeit",  # Fieldset title
                "availability_mo_am",
                "availability_tu_am",
                "availability_we_am",
                "availability_th_am",
                "availability_fr_am",
                "availability_mo_pm",
                "availability_tu_pm",
                "availability_we_pm",
                "availability_th_pm",
                "availability_fr_pm",
                "availability_comment",
            ),
            Submit("submit", "Speichern", css_class="btn btn-primary"),
        )
