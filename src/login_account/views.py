from django.shortcuts import render

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from login_account.forms import LoginForm
from django.contrib.auth import login
from .forms import TeacherForm, CandidateForm

from school_management.models import CustomUser


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request, username=data["username"], password=data["password"]
            )
            person = CustomUser.objects.get(user=user)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.info(request, f"Willkommen {person.first_name}.")
                    return redirect("index")
                else:
                    return HttpResponse("Disabled account")
            else:
                return HttpResponse("Invalid login")
    else:
        form = LoginForm()

    return render(request, "login_account/login.html", {"form": form})


@login_required
def user_logout(request):
    user = request.user
    try:
        person = CustomUser.objects.get(user=user)
        logout(request)
        messages.info(request, f"Auf Wiedersehen {person.first_name}.")
    except person.DoesNotExist:
        logout(request)
        messages.info(request, f"Auf Wiedersehen.")
    return redirect("index")


@login_required
def user_profile_old(request):
    print(request.method)
    user = request.user
    try:
        person = CustomUser.objects.get(user=user)
    except person.DoesNotExist:
        messages.error(request, "Profile not found.")
        return redirect("some_error_page")  # Handle the error appropriately

    if request.method == "POST":
        profile_form_valid = False
        password_change_form_valid = False

        if person.is_teacher:
            form = TeacherForm(request.POST, instance=person)
        elif person.is_candidate:
            form = CandidateForm(request.POST, instance=person)
        else:
            messages.error(request, "Invalid profile type.")
            return redirect("some_error_page")

        password_change_form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            form.save()
            profile_form_valid = True

        if password_change_form.is_valid():
            user = password_change_form.save()
            update_session_auth_hash(
                request, user
            )  # Important to keep the user logged in
            password_change_form_valid = True
            messages.success(request, "Password changed successfully.")

        if profile_form_valid or password_change_form_valid:
            return redirect("profile")  # Redirect to a profile success page
    else:
        if person.is_teacher:
            form = TeacherForm(instance=person)
        elif person.is_candidate:
            form = CandidateForm(instance=person)
        else:
            messages.error(request, "Invalid profile type.")
            return redirect("some_error_page")

        password_change_form = PasswordChangeForm(request.user)

    return render(
        request,
        "login_account/profile.html",
        {"form": form, "password_change_form": password_change_form},
    )


@login_required
def user_profile(request):
    print(request.method)
    user = request.user
    try:
        person = CustomUser.objects.get(user=user)
    except person.DoesNotExist:
        messages.error(request, "Profile not found.")
        return redirect("some_error_page")  # Handle the error appropriately

    if request.method == "POST":
        profile_form_valid = False
        password_change_form_valid = False

        if person.is_teacher:
            form = TeacherForm(request.POST, instance=person)
        elif person.is_candidate:
            form = CandidateForm(request.POST, instance=person)
        else:
            messages.error(request, "Invalid profile type.")
            return redirect("some_error_page")

        if form.is_valid():
            form.save()
            profile_form_valid = True
            messages.success(request, "Profile updated successfully.")
            return redirect("school_management:candidate_detail", pk=person.pk)

    else:
        if person.is_teacher:
            form = TeacherForm(instance=person)
        elif person.is_candidate:
            form = CandidateForm(instance=person)
        else:
            messages.error(request, "Invalid profile type.")
            return redirect("some_error_page")

    password_change_form = PasswordChangeForm(request.user)

    return render(
        request,
        "login_account/profile.html",
        {"form": form, "password_change_form": password_change_form},
    )
