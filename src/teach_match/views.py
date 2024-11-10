from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import (
    UserProfileForm,
)  # Make sure you have a form for updating user profile


def index(request):
    """
    Render the welcome page template.
    """
    return render(request, "school_management/index.html")


@login_required
def user_profile(request):
    if request.method == "POST":
        profile_form = ProfileEditForm(request.POST, instance=request.user.profile)
        password_change_form = PasswordChangeForm(request.user, request.POST)

        if profile_form.is_valid():
            profile_form.save()

        if password_change_form.is_valid():
            user = password_change_form.save()
            update_session_auth_hash(
                request, user
            )  # Important to keep the user logged in
            return redirect(
                "profile_edit"
            )  # Redirect to the same page or any other page

    else:
        profile_form = ProfileEditForm(instance=request.user.profile)
        password_change_form = PasswordChangeForm(request.user)

    return render(
        request,
        "profile_edit.html",
        {
            "form": profile_form,
            "password_change_form": password_change_form,
        },
    )
