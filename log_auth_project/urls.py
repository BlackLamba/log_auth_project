from django.contrib import admin
from django.urls import path, include

urlpatterns = [
	path("admin/", admin.site.urls),
	# Эндпоинты для пользователей (регистрация, логин, профиль).
	path("api/users/", include("apps.users.urls")),
	# Маковые объекты (posts и comments).
	path("api/", include("apps.mock_objects.urls")),
	# Админские инструменты.
	path("api/admin_tools/", include("apps.admin_tools.urls")),
]