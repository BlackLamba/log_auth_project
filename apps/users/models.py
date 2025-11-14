from django.db import models
from django.utils import timezone

class User(models.Model):
	"""Хранит данные о пользователе и его активности."""
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	middle_name = models.CharField(max_length=100, blank=True, null=True)

	email = models.EmailField(unique=True)
	password_hash = models.CharField(max_length=255)

	is_active = models.BooleanField(default=True)

	created_at = models.DateTimeField(default=timezone.now)
	updated_at = models.DateTimeField(auto_now=True)

	objects = models.Manager()

	def __str__(self):
		return f"{self.email}"


class Role(models.Model):
	"""Роли пользователей."""
	name = models.CharField(max_length=50, unique=True)

	objects = models.Manager()

	def __str__(self):
		return self.name


class Permission(models.Model):
	"""Права на действия с различными ресурсами."""
	resource = models.CharField(max_length=100)
	action = models.CharField(max_length=100)

	objects = models.Manager()

	class Meta:
		unique_together = ("resource", "action") # Уникальность права.

	def __str__(self):
		return f"{self.resource}:{self.action}"


class UserRole(models.Model):
	"""Кто и какую роль имеет."""
	user = models.ForeignKey("User", on_delete=models.CASCADE)
	role = models.ForeignKey("Role", on_delete=models.CASCADE)

	objects = models.Manager()

	class Meta:
		unique_together = ("user", "role") # Уникальность роли для пользователя.


class RolePermission(models.Model):
	"""Какая роль имеет эти права."""
	role = models.ForeignKey("Role", on_delete=models.CASCADE)
	permission = models.ForeignKey("Permission", on_delete=models.CASCADE)

	objects = models.Manager()

	class Meta:
		unique_together = ("role", "permission") # Уникальность права для роли.
