from .models import UserRole, RolePermission, Permission

def has_permission(user_id: int, resource: str, action: str) -> bool:
	"""Проверяем, есть ли у пользователя право на действие с ресурсом."""
	# Получение ролей пользователя.
	roles = UserRole.objects.filter(user_id=user_id).values_list("role_id", flat=True)
	if not roles:
		return False

	# Получение прав ролей.
	permissions = RolePermission.objects.filter(role_id__in=roles).values_list("permission_id", flat=True)
	if not permissions:
		return False

	# Проверка, есть ли право на конкретный ресурс.
	return Permission.objects.filter(id__in=permissions, resource=resource, action=action).exists()
