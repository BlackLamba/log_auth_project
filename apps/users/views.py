from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import User
from .utils import hash_password, verify_password, generate_token, verify_token, invalidate_token


# Вспомогательные функции.

def get_user_from_token(request):
    """Проверка токена и получение пользователя."""
    token = request.headers.get("Authorization")
    if not token:
        return None, Response({"error": "Токен обязателен"}, status=status.HTTP_401_UNAUTHORIZED)

    user_id = verify_token(token)
    if not user_id:
        return None, Response({"error": "Неверный или просроченный токен"}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None, Response({"error": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)

    return user, None


def validate_registration_data(data):
    """Валидация данных для регистрации."""
    required_fields = ["email", "password", "password2", "first_name", "last_name"]
    for field in required_fields:
        if not data.get(field):
            return {"error": f"Поле {field} обязательно"}

    if data["password"] != data["password2"]:
        return {"error": "Пароли не совпадают"}

    if User.objects.filter(email=data["email"]).exists():
        return {"error": "Пользователь с таким email уже существует"}

    return None


# Представления.

class RegisterView(APIView):
    def post(self, request):
        """Регистрация нового пользователя."""
        data = request.data
        error = validate_registration_data(data)
        if error:
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create(
            email=data["email"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            middle_name=data.get("middle_name", ""),
            password_hash=hash_password(data["password"]),
        )
        return Response({"message": "Пользователь успешно зарегистрирован"}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):
        """Логин в систему."""
        data = request.data
        email = data.get("email")
        password = data.get("password")

        if not all([email, password]):
            return Response({"error": "Email и пароль обязательны"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email, is_active=True)
        except User.DoesNotExist:
            return Response({"error": "Неверный email или пароль"}, status=status.HTTP_401_UNAUTHORIZED)

        if not verify_password(password, user.password_hash):
            return Response({"error": "Неверный email или пароль"}, status=status.HTTP_401_UNAUTHORIZED)

        token = generate_token(user.id)
        return Response({"token": token})


class LogoutView(APIView):
    def post(self, request):
        """Логаут из системы."""
        token = request.headers.get("Authorization")
        if not token:
            return Response({"error": "Токен обязателен"}, status=status.HTTP_401_UNAUTHORIZED)

        invalidate_token(token)
        return Response({"message": "Вы успешно вышли из системы"})


class ProfileView(APIView):
    """Получение, изменение и удаление данных о профиле."""

    def get(self, request):
        user, error = get_user_from_token(request)
        if error:
            return error

        return Response({
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "middle_name": user.middle_name,
        })

    def put(self, request):
        user, error = get_user_from_token(request)
        if error:
            return error

        data = request.data
        for field in ["first_name", "last_name", "middle_name"]:
            setattr(user, field, data.get(field, getattr(user, field)))
        user.save()
        return Response({"message": "Профиль обновлён"})

    def delete(self, request):
        user, error = get_user_from_token(request)
        if error:
            return error

        user.is_active = False
        user.save()
        invalidate_token(request.headers.get("Authorization"))
        return Response({"message": "Аккаунт удалён"})