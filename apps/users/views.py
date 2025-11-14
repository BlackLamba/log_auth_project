from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import User
from .utils import hash_password, verify_password, generate_token, verify_token, invalidate_token


# Регистрация.
class RegisterView(APIView):
	def post(self, request):
		"""Регистрация нового пользователя."""
		data = request.data
		email = data.get("email")
		password = data.get("password")
		password2 = data.get("password2")
		first_name = data.get("first_name")
		last_name = data.get("last_name")
		middle_name = data.get("middle_name", "")

		if not all([email, password, password2, first_name, last_name]):
			return Response({"error": "Не все поля заполнены"},
							status=status.HTTP_400_BAD_REQUEST)

		if password != password2:
			return Response({"error": "Пароли не совпадают"},
							status=status.HTTP_400_BAD_REQUEST)

		if User.objects.filter(email=email).exists():
			return Response({"error": "Пользователь с таким email уже существует"},
							status=status.HTTP_400_BAD_REQUEST)

		user = User.objects.create(
			email = email,
			first_name = first_name,
			last_name = last_name,
			middle_name = middle_name,
			password_hash = hash_password(password),
		)

		return Response({"message": "Пользователь успешно зарегистрирован"},
						status=status.HTTP_201_CREATED)

# Вход в систему.
class LoginView(APIView):
	def post(self, request):
		"""Логин в систему."""
		data = request.data
		email = data.get("email")
		password = data.get("password")

		if not all([email, password]):
			return Response({"error": "Email и пароль обязательны"},
							status=status.HTTP_400_BAD_REQUEST)

		try:
			user = User.objects.get(email=email, is_active=True)
		except User.DoesNotExist:
			return Response({"error": "Неверный email или пароль"},
							status=status.HTTP_401_UNAUTHORIZED)

		if not verify_password(password, user.password_hash):
			return Response({"error": "Неверный email или пароль"},
							status=status.HTTP_401_UNAUTHORIZED)

		token = generate_token(user.id)
		return Response({"token": token})


# Выход из системы.
class LogoutView(APIView):
	def post(self, request):
		"""Логаут из системы."""
		token = request.headers.get("Authorization")
		if not token:
			return Response({"error": "Токен обязателен"},
							status=status.HTTP_401_UNAUTHORIZED)

		invalidate_token(token)
		return Response({"message": "Вы успешно вышли из системы"})

# Профиль.
class ProfileView(APIView):
	def get(self, request):
		"""Получение данных о профиле."""
		token = request.headers.get("Authorization")
		user_id = verify_token(token)
		if not user_id:
			return Response({"error": "Неверный или просроченный токен"},
							status=status.HTTP_401_UNAUTHORIZED)

		user = User.objects.get(id=user_id)
		return Response({
			"email": user.email,
			"first_name": user.first_name,
			"last_name": user.last_name,
			"middle_name": user.middle_name,
		})

	def put(self, request):
		"""Изменение данных профиля."""
		token = request.headers.get('Authorization')
		user_id = verify_token(token)
		if not user_id:
			return Response({"error": "Неверный или просроченный токен"},
							status=status.HTTP_401_UNAUTHORIZED)

		user = User.objects.get(id=user_id)
		data = request.data
		user.first_name = data.get("first_name", user.first_name)
		user.last_name = data.get("last_name", user.last_name)
		user.middle_name = data.get("middle_name", user.middle_name)
		user.save()
		return Response({"message": "Профиль обновлён"})

	def delete(self, request):
		"""Удаление профиля."""
		token = request.headers.get('Authorization')
		user_id = verify_token(token)
		if not user_id:
			return Response({"error": "Неверный или просроченный токен"},
							status=status.HTTP_401_UNAUTHORIZED)

		user = User.objects.get(id=user_id)
		user.is_active = False
		user.save()
		invalidate_token(token)
		return Response({"message": "Аккаунт удалён"})