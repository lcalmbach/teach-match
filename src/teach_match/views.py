from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import UserProfileForm  # Make sure you have a form for updating user profile


def index(request):
    """
    Render the welcome page template.
    """
    return render(request, 'school_management/index.html')

@login_required
def user_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'user_profile.html', {'form': form})