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
    SubstitutionCreateWithTeacherView,
    SubstitutionCandidatesListView,
    TeacherListView,
    TeacherDetailView,
    TeacherEditView,
    ApplicationCreateView,
    InviteCandidatesView,
    AcceptInvitationView,
    admin_tasks,
    calculate_teacher_availability,
    ApplicationListView,
    ApplicationDetailView,
    ApplicationEditView,
    CandidateCreateView,
    CandidateDeleteView,
    InviteCandidatesView,
    InvitationDetailView,
    AddExecutedByView
)

app_name = "school_management"

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
    path(
        "substitutions_admin/",
        SubstitutionAdminListView.as_view(),
        name="substitution_admin_list",
    ),
    path(
        "substitution/<int:pk>/",
        SubstitutionDetailView.as_view(),
        name="substitution_detail",
    ),
    path(
        "substitution/<int:pk>/edit/",
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
        SubstitutionCreateWithTeacherView.as_view(),
        name="substitution_create_with_teacher",
    ),
    path(
        "substitutions_candidates/",
        SubstitutionCandidatesListView.as_view(),
        name="substitution_candidates_list",
    ),
    path("admin-tasks/", admin_tasks, name="admin_tasks"),
    path(
        "calculate-availability/",
        calculate_teacher_availability,
        name="calculate_availability",
    ),
    path("find_match/", SubstitutionAdminListView.as_view(), name="find_match"),
    path("login/", SubstitutionEditView.as_view(), name="login"),
    path(
        "application/create/<int:id>/",
        ApplicationCreateView.as_view(),
        name="application_create",
    ),
    path("invitation/<int:id>/", InviteCandidatesView.as_view(), name="invitation_create"),
    path("invitation_accept/<int:id>/", AcceptInvitationView.as_view(), name="invitation_accept"),
    path("applications/", ApplicationListView.as_view(), name="application_list"),
    path(
        "applications/<int:pk>/",
        ApplicationDetailView.as_view(),
        name="application_detail",
    ),
    path(
        "invitations/<int:pk>/",
        InvitationDetailView.as_view(),
        name="invitation_detail",
    ),
    path(
        "applications/edit/<int:pk>/",
        ApplicationEditView.as_view(),
        name="application_edit",
    ),
    path("candidate/create/", CandidateCreateView.as_view(), name="candidate_create"),
    path(
        "candidate/delete/<int:pk>/",
        CandidateDeleteView.as_view(),
        name="candidate_delete",
    ),
    path(
        "substitution/<int:substitution_id>/add_executed_by/",
        AddExecutedByView.as_view(),
        name="add_executed_by",
    ),

]