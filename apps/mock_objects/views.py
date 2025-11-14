from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.users.utils import verify_token
from apps.users.permissions import has_permission

# Моковые посты и комментарии.
POSTS = [
	{"id": 1, "title": "Первый пост"},
	{"id": 2, "title": "Второй пост"},
]

COMMENTS = [
	{"id": 1, "post_id": 1, "text": "Первый комментарий"},
	{"id": 2, "post_id": 1, "text": "Первый комментарий"},
]

# Вспомогательные функции.

def authorize_request(request, resource, action):
	"""Проверяет токен и права пользователя. Возвращает user_id или Response с ошибкой."""
	token = request.headers.get('Authorization')
	user_id = verify_token(token)
	if not user_id:
		return None, Response({"error": "Не авторизован"}, status=status.HTTP_401_UNAUTHORIZED)

	if not has_permission(user_id, resource=resource, action=action):
		return None, Response({"error": "Доступ запрещён"}, status=status.HTTP_403_FORBIDDEN)

	return user_id, None

# Посты.
class PostsView(APIView):
    def get(self, request):
        user_id, error = authorize_request(request, resource="posts", action="read")
        if error:
            return error
        return Response({"posts": POSTS})

    def post(self, request):
        user_id, error = authorize_request(request, resource="posts", action="write")
        if error:
            return error

        data = request.data
        new_post = {
            "id": len(POSTS) + 1,
            "title": data.get("title", "")
        }
        POSTS.append(new_post)
        return Response(new_post, status=status.HTTP_201_CREATED)


# Комментарии.
class CommentsView(APIView):
    def get(self, request):
        user_id, error = authorize_request(request, resource="comments", action="read")
        if error:
            return error
        return Response({"comments": COMMENTS})

    def post(self, request):
        user_id, error = authorize_request(request, resource="comments", action="write")
        if error:
            return error

        data = request.data
        new_comment = {
            "id": len(COMMENTS) + 1,
            "post_id": data.get("post_id"),
            "text": data.get("text", "")
        }
        COMMENTS.append(new_comment)
        return Response(new_comment, status=status.HTTP_201_CREATED)