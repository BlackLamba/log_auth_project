import os
import django


# Настройка Django для использования скрипта вне сервера.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "log_auth_project.settings")
django.setup()

from apps.users.models import User, Role, Permission, UserRole, RolePermission
from apps.users.utils import hash_password

# Очистка таблиц.
UserRole.objects.all().delete()
RolePermission.objects.all().delete()
User.objects.all().delete()
Role.objects.all().delete()
Permission.objects.all().delete()

# Создание ролей.
admin_role = Role.objects.create(name="admin")
user_role = Role.objects.create(name="user")
editor_role = Role.objects.create(name='editor')

# Создание прав.
perm_read_posts = Permission.objects.create(resource='posts', action="read")
perm_write_posts = Permission.objects.create(resource='posts', action="write")
perm_read_comments = Permission.objects.create(resource='comments', action="read")
perm_write_comments = Permission.objects.create(resource='comments', action="write")

# Назначение прав ролям.
RolePermission.objects.create(role=admin_role, permission=perm_read_posts)
RolePermission.objects.create(role=admin_role, permission=perm_write_posts)
RolePermission.objects.create(role=admin_role, permission=perm_read_comments)
RolePermission.objects.create(role=admin_role, permission=perm_write_comments)

RolePermission.objects.create(role=user_role, permission=perm_read_posts)
RolePermission.objects.create(role=user_role, permission=perm_read_comments)

RolePermission.objects.create(role=editor_role, permission=perm_read_posts)
RolePermission.objects.create(role=editor_role, permission=perm_write_posts)
RolePermission.objects.create(role=editor_role, permission=perm_read_comments)

# Создание пользователей.
admin_user = User.objects.create(
	first_name="Admin",
	last_name="Super",
	email="admin@admin.com",
	password_hash=hash_password("superadmin"),
	is_active=True
)

com_user = User.objects.create(
	first_name="Alex",
	last_name="Dobrynya",
	email="user@user.com",
	password_hash=hash_password("superuser"),
	is_active=True
)

editor_user = User.objects.create(
	first_name="Mystic",
	last_name="Editor",
	email="editor@editor.com",
	password_hash=hash_password("supereditor"),
	is_active=True
)

# Назначение ролей пользователям.
UserRole.objects.create(user=admin_user, role=admin_role)
UserRole.objects.create(user=com_user, role=user_role)
UserRole.objects.create(user=editor_user, role=editor_role)

print("Пользователи:")
print("Admin: admin@example.com / admin123")
print("User: user@example.com / user123")
print("Editor: editor@example.com / editor123")