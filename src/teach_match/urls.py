"""
URL configuration for teach_match project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views  
from django.conf.urls.static import static
from django.conf import settings
from django.shortcuts import redirect

def redirect_to_substitution_candidates(request):
    return redirect('school_management/substitution_candidates/', permanent=True)

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', redirect_to_substitution_candidates, name='index'),
    path('school_management/', include('school_management.urls')),
    path('login/', include('login_account.urls')),
    # ... other URL patterns ...
    path('profile/', views.user_profile, name='user_profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)