from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from school_management.models import Teacher, Candidate, Subject
from crispy_forms.helper import FormHelper


class SignUpForm(UserCreationForm):
    bio = forms.CharField(max_length=500, required=False, help_text='Optional.')
    location = forms.CharField(max_length=30, required=False, help_text='Ort.')

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name', 'bio')
        labels = {
            'username': 'Benutzername',
            'password': 'Passwort',
            'password2': 'Passwort bestätigen',
            'first_name': 'Vorname',
            'last_name': 'Nachname'
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.save()
        profile = Profile.objects.get(user=user)
        profile.bio = self.cleaned_data['bio']
        profile.location = self.cleaned_data['location']
        if commit:
            profile.save()
        return user

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        for field in self.fields.values():
            if field.help_text:
                field.widget.attrs.update({'title': field.help_text})
                field.help_text = ''


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = [
            'first_name', 
            'last_name', 
        ]  # Replace with actual fields for teachers


class CandidateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["subjects"].widget.attrs.update(size="20")

    class Meta:
        model = Candidate
        fields = [
            'first_name', 
            'last_name', 
            'available_from_date', 
            'available_to_date',
            
            'availability_mo_am',
            'availability_tu_am',
            'availability_we_am',
            'availability_th_am',
            'availability_fr_am',
            'availability_mo_pm',
            'availability_tu_pm',
            'availability_we_pm',
            'availability_th_pm',
            'availability_fr_pm',
            'subjects',
        ] 

        widgets = {
            "available_from_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}, format='%Y-%m-%d'),
            "available_to_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}, format='%Y-%m-%d'),
        }
        subjects = forms.ModelMultipleChoiceField(
            queryset=Subject.objects.all(),
            widget=forms.SelectMultiple(),
            # widget=forms.SelectMultiple(attrs={'class': 'form-select'}) 
            required=False
        )
        
