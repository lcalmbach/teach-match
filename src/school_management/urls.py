from django.urls import path
from .views import SchoolDetailView, SchoolListView, SchoolEditView
from .views import (
    CandidateListView,
    CandidateEditView,
    CandidateDetailView,
    SubstitutionListView,
    SubstitutionDetailView,
    SubstitutionEditView,
    SubstitutionCreateView,
    TeacherListView,
    TeacherDetailView,
    TeacherEditView,
)

urlpatterns = [
    path("schools/", SchoolListView.as_view(), name="school_list"),
    path("schools/<int:pk>/", SchoolDetailView.as_view(), name="school_detail"),
    path("schools/<int:pk>/edit/", SchoolEditView.as_view(), name="school_edit"),
    path("candidates/", CandidateListView.as_view(), name="candidate_list"),
    path(
        "candidates/<int:pk>/", CandidateDetailView.as_view(), name="candidate_detail"
    ),
    path(
        "candidates/<int:pk>/edit/", CandidateEditView.as_view(), name="candidate_edit"
    ),
    path("teachers/", TeacherListView.as_view(), name="teacher_list"),
    path("teachers/<int:pk>/", TeacherDetailView.as_view(), name="teacher_detail"),
    path("teachers/<int:pk>/edit/", TeacherEditView.as_view(), name="teacher_edit"),
    
    path("substitutions/", SubstitutionListView.as_view(), name="substitution_list"),
    path(
        "substitutions/<int:pk>/",
        SubstitutionDetailView.as_view(),
        name="substitution_detail",
    ),
    path('substitution/<int:pk>/', SubstitutionEditView.as_view(), name='substitution_edit'),  # For editing
    path('substitution/new/', SubstitutionCreateView.as_view(), name='substitution_create'),  # For creating new

    path("find_match/", SubstitutionListView.as_view(), name="find_match"),
    path("login/", SubstitutionEditView.as_view(), name="login"),
]
