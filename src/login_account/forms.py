from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
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
