from django.urls import path
from .views import SchoolDetailView, SchoolListView, SchoolEditView
from .views import (
    CandidateListView,
    CandidateEditView,
    CandidateDetailView,
    
    SubstitutionAdminListView,
    SubstitutionDetailView,
    SubstitutionEditView,
    SubstitutionCreateView,
    SubstitutionCandidatesListView,

    TeacherListView,
    TeacherDetailView,
    TeacherEditView,
    ApplicationCreateView,
    InvitationCreateView
)

app_name = 'school_management'

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
    
    path("substitutions_admin/", SubstitutionAdminListView.as_view(), name="substitution_admin_list"),
    path(
        "substitutions/<int:pk>/",
        SubstitutionDetailView.as_view(),
        name="substitution_detail",
    ),
    
    path(
        "substitution/<int:pk>/",
        SubstitutionEditView.as_view(),
        name="substitution_edit",
    ),  
    path(
        "substitution/new/",
        SubstitutionCreateView.as_view(),
        name="substitution_create",
    ),  
    path(
        "substitution/new/<int:teacher_id>/",
        SubstitutionCreateView.as_view(),
        name="substitution_create_with_teacher",
    ),
    path("substitutions_candidates/", SubstitutionCandidatesListView.as_view(), name="substitution_candidates_list"),
    
    path("find_match/", SubstitutionAdminListView.as_view(), name="find_match"),
    path("login/", SubstitutionEditView.as_view(), name="login"),
    path('application/create/<int:id>/', ApplicationCreateView.as_view(), name='application_create'),
    path("invitation/", InvitationCreateView.as_view(), name="invitation_create"),
]
