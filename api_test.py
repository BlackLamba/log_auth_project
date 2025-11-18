import requests

BASE_URL = "http://127.0.0.1:8000/api"

# Пользователи из seed_db.py.
users = {
    "admin": {"email": "admin@admin.com", "password": "superadmin"},
    "user": {"email": "user@user.com", "password": "superuser"},
    "editor": {"email": "editor@editor.com", "password": "supereditor"}
}


# Вспомогательные функции.

def make_request(method, endpoint, token=None, json_data=None):
    """Отправляет HTTP-запрос и возвращает статус и JSON-данные."""
    headers = {"Authorization": token} if token else {}
    url = f"{BASE_URL}/{endpoint}/"
    resp = requests.request(method, url, headers=headers, json=json_data)
    data = resp.json() if resp.content else {}
    return resp.status_code, data


def print_result(role, method, endpoint, status_code, data):
    """Вывод результата запроса в консоль."""
    if status_code in (401, 403):
        print(f"{role}: {method} /{endpoint}/ -> {status_code} {data.get('error', '')}")
    else:
        print(f"{role}: {method} /{endpoint}/ -> {status_code}, {data}")


def login(email, password):
    """Логин пользователя, возвращает токен."""
    status_code, data = make_request("POST", "users/login", json_data={"email": email, "password": password})
    if status_code == 200:
        token = data.get("token")
        print(f"Login successful: {email}")
        return token
    else:
        print(f"Login failed: {email}, status: {status_code}")
        return None


# Тесты ресурсов.

def test_resource(token, role, resource, post_data=None):
    """Тест GET и POST для ресурса (posts, comments)."""
    # GET
    status_code, data = make_request("GET", resource, token)
    print_result(role, "GET", resource, status_code, data)

    # POST
    if post_data:
        status_code, data = make_request("POST", resource, token, json_data=post_data)
        print_result(role, "POST", resource, status_code, data)


def test_admin_tools(token, role):
    """Тестирование эндпоинта админских инструментов."""
    status_code, data = make_request("GET", "admin_tools/overview", token)
    print_result(role, "GET", "admin_tools/overview", status_code, data)


def test_profile(token, role):
    """Тестирование профиля пользователя: GET, PUT, DELETE."""
    # GET
    status_code, data = make_request("GET", "users/profile", token)
    print_result(role, "GET", "profile", status_code, data)

    # PUT
    update_data = {"first_name": f"{role}_new"}
    status_code, data = make_request("PUT", "users/profile", token, json_data=update_data)
    print_result(role, "PUT", "profile", status_code, data)

    # DELETE
    status_code, data = make_request("DELETE", "users/profile", token)
    print_result(role, "DELETE", "profile", status_code, data)


def test_unauthorized():
    """Проверка доступа без токена (должны быть 401)."""
    print("\nПроверка без токена (должен быть 401)")
    for endpoint in ["posts", "comments", "admin_tools/overview", "users/profile"]:
        status_code, data = make_request("GET", endpoint)
        print(f"{endpoint}: GET -> {status_code}, {data}")


# Основной тестовый сценарий

if __name__ == "__main__":
    # Проверка 401 без токена
    test_unauthorized()

    # Тестируем каждого пользователя
    for role, creds in users.items():
        print(f"\nТестирование для пользователя: {role}")
        token = login(creds["email"], creds["password"])
        if token:
            test_resource(token, role, "posts", {"title": "Новый пост"})
            test_resource(token, role, "comments", {"post_id": 1, "text": "Новый комментарий"})
            test_admin_tools(token, role)
            test_profile(token, role)