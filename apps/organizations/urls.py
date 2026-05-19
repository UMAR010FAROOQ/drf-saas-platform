from django.urls import path
from .views import OrganizationCreateView, OrganizationListView, OrgDashboardView, OrgManageView

urlpatterns = [
    path("", OrganizationListView.as_view()),
    path("create/", OrganizationCreateView.as_view()),

    path("dashboard/", OrgDashboardView.as_view()),
    path("manage/", OrgManageView.as_view()),
]