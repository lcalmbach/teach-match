from django.shortcuts import render


def index(request):
    """
    Render the welcome page template.
    """
    return render(request, 'school_management/index.html')