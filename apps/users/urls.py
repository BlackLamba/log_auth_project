from django.urls import path

# Эндпоинты.

from .views import RegisterView, LogoutView, ProfileView, LoginView

urlpatterns = [
	path("register/", RegisterView.as_view()),
	path("login/", LoginView.as_view()),
	path("logout/", LogoutView.as_view()),
	path("profile/", ProfileView.as_view())
]