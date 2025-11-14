from django.urls import path
from .views import PostsView, CommentsView


urlpatterns = [
	path("posts/", PostsView.as_view()),
	path("comments/", CommentsView.as_view()),
]