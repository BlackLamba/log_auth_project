from django.urls import path
from .views import UserRoleView, RolePermissionView, AdminOverviewView

urlpatterns = [
	path("user_roles/", UserRoleView.as_view()),
	path("role_permissions/", RolePermissionView.as_view()),
	path("overview/", AdminOverviewView.as_view()),
]