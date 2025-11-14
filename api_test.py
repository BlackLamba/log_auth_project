import requests

BASE_URL = "http://127.0.0.1:8000/api"

# Пользователи из seed_db.py.
users = {
    "admin": {"email": "admin@admin.com", "password": "superadmin"},
    "user": {"email": "user@user.com", "password": "superuser"},
    "editor": {"email": "editor@editor.com", "password": "supereditor"}
}

# Логин.
def login(email, password):
    resp = requests.post(f"{BASE_URL}/users/login/", json={"email": email, "password": password})
    if resp.status_code == 200:
        token = resp.json().get("token")
        print(f"Login successful: {email}")
        return token
    else:
        print(f"Login failed: {email}, status: {resp.status_code}")
        return None

# Тест постов.
def test_posts(token, role):
    headers = {"Authorization": token} if token else {}

    r = requests.get(f"{BASE_URL}/posts/", headers=headers)
    if r.status_code == 403:
        print(f"{role}: GET /posts/ -> 403 Forbidden")
    else:
        print(f"{role}: GET /posts/ -> {r.status_code}, {r.json()}")

    r = requests.post(f"{BASE_URL}/posts/", headers=headers, json={"title": "Новый пост"})
    if r.status_code == 403:
        print(f"{role}: POST /posts/ -> 403 Forbidden")
    else:
        print(f"{role}: POST /posts/ -> {r.status_code}, {r.json()}")

# Тест комментариев.
def test_comments(token, role):
    headers = {"Authorization": token} if token else {}

    r = requests.get(f"{BASE_URL}/comments/", headers=headers)
    if r.status_code == 403:
        print(f"{role}: GET /comments/ -> 403 Forbidden")
    else:
        print(f"{role}: GET /comments/ -> {r.status_code}, {r.json()}")

    r = requests.post(f"{BASE_URL}/comments/", headers=headers, json={"post_id": 1, "text": "Новый комментарий"})
    if r.status_code == 403:
        print(f"{role}: POST /comments/ -> 403 Forbidden")
    else:
        print(f"{role}: POST /comments/ -> {r.status_code}, {r.json()}")

# Тест admin_tools.
def test_admin_tools(token, role):
    headers = {"Authorization": token} if token else {}

    r = requests.get(f"{BASE_URL}/admin_tools/overview/", headers=headers)
    if r.status_code == 403:
        print(f"{role}: GET /admin_tools/overview/ -> 403 Forbidden")
    else:
        print(f"{role}: GET /admin_tools/overview/ -> {r.status_code}, {r.json()}")

# Проверка без токена (401).
def test_unauthorized():
    print("\n Проверка без токена (должен быть 401) ")
    for endpoint in ["posts", "comments", "admin_tools/overview"]:
        r = requests.get(f"{BASE_URL}/{endpoint}/")
        print(f"{endpoint}: GET -> {r.status_code}, {r.json()}")

def test_profile(token, role):
    headers = {"Authorization": token} if token else {}

    # GET /users/profile/
    r = requests.get(f"{BASE_URL}/users/profile/", headers=headers)
    if r.status_code == 401:
        print(f"{role}: GET /profile/ -> 401 Unauthorized")
    else:
        print(f"{role}: GET /profile/ -> {r.status_code}, {r.json()}")

    # PUT /users/profile/ - обновление имени
    update_data = {"first_name": f"{role}_new"}
    r = requests.put(f"{BASE_URL}/users/profile/", headers=headers, json=update_data)
    if r.status_code == 401:
        print(f"{role}: PUT /profile/ -> 401 Unauthorized")
    else:
        print(f"{role}: PUT /profile/ -> {r.status_code}, {r.json()}")

    # DELETE /users/profile/ - мягкое удаление
    r = requests.delete(f"{BASE_URL}/users/profile/", headers=headers)
    if r.status_code == 401:
        print(f"{role}: DELETE /profile/ -> 401 Unauthorized")
    else:
        print(f"{role}: DELETE /profile/ -> {r.status_code}, {r.json()}")

# Основной тест.
if __name__ == "__main__":
    # Проверка 401.
    test_unauthorized()

    # Тестируем каждого пользователя.
    for role, creds in users.items():
        print(f"\nТестирование для пользователя: {role}")
        token = login(creds["email"], creds["password"])
        if token:
            test_posts(token, role)
            test_comments(token, role)
            test_admin_tools(token, role)
            test_profile(token, role)