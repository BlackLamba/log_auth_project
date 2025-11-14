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


# Посты.
class PostsView(APIView):
	def get(self, request):
		token = request.headers.get('Authorization')
		user_id = verify_token(token)
		if not user_id:
			return Response({"error": "Не авторизован"},
							status=status.HTTP_401_UNAUTHORIZED)

		if not has_permission(user_id, resource="posts", action="read"):
			return Response({"error": "Доступ запрещён"},
							status=status.HTTP_403_FORBIDDEN)

		return Response({"posts": POSTS})

	def post(self, request):
		token = request.headers.get('Authorization')
		user_id = verify_token(token)
		if not user_id:
			return Response({"error": "Не авторизован"},
							status=status.HTTP_401_UNAUTHORIZED)

		if not has_permission(user_id, resource="posts", action="write"):
			return Response({"error": "Доступ запрещён"},
							status=status.HTTP_403_FORBIDDEN)

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
		token = request.headers.get('Authorization')
		user_id = verify_token(token)
		if not user_id:
			return Response({"error": "Не авторизован"},
							status=status.HTTP_401_UNAUTHORIZED)

		if not has_permission(user_id, resource="comments", action="read"):
			return Response({"error": "Доступ запрещён"},
							status=status.HTTP_403_FORBIDDEN)

		return Response({"posts": COMMENTS})

	def post(self, request):
		token = request.headers.get('Authorization')
		user_id = verify_token(token)
		if not user_id:
			return Response({"error": "Не авторизован"},
							status=status.HTTP_401_UNAUTHORIZED)

		if not has_permission(user_id, resource="comments", action="write"):
			return Response({"error": "Доступ запрещён"},
							status=status.HTTP_403_FORBIDDEN)

		data = request.data
		new_comment = {
			"id": len(COMMENTS) + 1,
			"post_id": data.get("post_id"),
			"text": data.get("text", "")
		}
		COMMENTS.append(new_comment)
		return Response(new_comment, status=status.HTTP_201_CREATED)

