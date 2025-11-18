from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.users.models import User, UserRole, RolePermission
from apps.users.utils import verify_token

# Роль "admin" дает право на все действия с admin_tools
ADMIN_ROLE_NAME = "admin"

# Вспомогательные функции.

def require_admin(func):
    """Декоратор для проверки токена и прав администратора."""
    def wrapper(self, request, *args, **kwargs):
        token = request.headers.get("Authorization")
        user_id = verify_token(token)
        if not user_id or not is_admin(user_id):
            return Response({"error": "Доступ запрещен"}, status=status.HTTP_403_FORBIDDEN)
        request.user_id = user_id
        return func(self, request, *args, **kwargs)
    return wrapper

def is_admin(user_id):
    """Проверяем, является ли пользователь администратором."""
    roles = UserRole.objects.filter(user_id=user_id).select_related("role")
    return any(r.role.name == ADMIN_ROLE_NAME for r in roles)

# Управление ролями пользователя.
class UserRoleView(APIView):

    @require_admin
    def post(self, request):
        """Назначить роль пользователю."""
        target_user_id = request.data.get("user_id")
        role_id = request.data.get("role_id")

        if UserRole.objects.filter(user_id=target_user_id, role_id=role_id).exists():
            return Response({"error": "Роль уже назначена"}, status=status.HTTP_400_BAD_REQUEST)

        UserRole.objects.create(user_id=target_user_id, role_id=role_id)
        return Response({"message": "Роль назначена"})

    @require_admin
    def delete(self, request):
        """Удалить роль у пользователя."""
        target_user_id = request.data.get("user_id")
        role_id = request.data.get("role_id")

        UserRole.objects.filter(user_id=target_user_id, role_id=role_id).delete()
        return Response({"message": "Роль удалена"})

# Управление правами роли.
class RolePermissionView(APIView):

    @require_admin
    def post(self, request):
        """Добавить право для роли."""
        role_id = request.data.get("role_id")
        permission_id = request.data.get("permission_id")

        if RolePermission.objects.filter(role_id=role_id, permission_id=permission_id).exists():
            return Response({"error": "Право уже назначено"}, status=status.HTTP_400_BAD_REQUEST)

        RolePermission.objects.create(role_id=role_id, permission_id=permission_id)
        return Response({"message": "Право добавлено"})

    @require_admin
    def delete(self, request):
        """Удалить право у роли."""
        role_id = request.data.get("role_id")
        permission_id = request.data.get("permission_id")

        RolePermission.objects.filter(role_id=role_id, permission_id=permission_id).delete()
        return Response({"message": "Право удалено"})

# Получение ролей и прав.
class AdminOverviewView(APIView):
    """Список всех пользователей с их ролями и правами."""

    @require_admin
    def get(self, request):
        users_data = []

        users = User.objects.filter(is_active=True)
        for u in users:
            roles = UserRole.objects.filter(user=u).select_related("role")
            roles_data = []
            for r in roles:
                perms = RolePermission.objects.filter(role=r.role).select_related("permission")
                perms_data = [{"resource": p.permission.resource, "action": p.permission.action} for p in perms]
                roles_data.append({"role": r.role.name, "permissions": perms_data})
            users_data.append({"user_id": u.id, "email": u.email, "roles": roles_data})

        return Response(users_data)



