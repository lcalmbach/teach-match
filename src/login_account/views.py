from django.shortcuts import render

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from login_account.forms import LoginForm
from django.contrib.auth import login
from .forms import SignUpForm

from school_management.models import Person

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data['username'], password=data['password'])
            person = Person.objects.get(user=user)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.info(request, f"Willkommen {person.first_name}.")
                    return redirect('index')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()

    return render(request, 'login_account/login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.info(request, f"Auf Wiedersehen {person.first_name}.")
    return redirect('index')


def user_signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirect to a home page or other appropriate page
    else:
        form = SignUpForm()
    return render(request, 'login_account/signup.html', {'form': form})
