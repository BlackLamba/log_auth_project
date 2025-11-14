import bcrypt
import uuid
from datetime import datetime, timedelta

# Здесь будут храниться активные токены в памяти для примера.
active_tokens = {}

# Пароль.
def hash_password(password: str) -> str:
	"""Хеширование пароля с помощью bcrypt."""
	salt = bcrypt.gensalt()
	hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
	return  hashed.decode('utf-8')


def verify_password(password: str, hashed: str) -> bool:
	"""Проверка пароля."""
	return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

# Токены.
def generate_token(user_id: int, expires_in: int = 3600) -> str:
	"""
	Генерируем уникальный токен для пользователя.
	expires_in - время жизни токена в сек.
	"""
	token = str(uuid.uuid4())
	expiry = datetime.utcnow() + timedelta(seconds=expires_in)
	# Сохраняем токен и время жизни.
	active_tokens[token] = {"user_id": user_id, "expires_at": expiry}
	return token

def verify_token(token: str) -> int | None:
	"""Проверка токена. Возвращаем user_id если токен валиден."""
	data = active_tokens.get(token)
	if not data:
		return None

	if datetime.utcnow() > data["expires_at"]:
		# Токен просрочен, удаляем.
		del active_tokens[token]
		return None

	return data["user_id"]

def invalidate_token(token: str):
	"""Удаляем токен для logout."""
	active_tokens.pop(token, None)