from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("liked", views.liked_api, name="liked"),
    path("posts", views.post_view, name="posts"),
    path("user/<int:id>", views.user_profile_view, name="user_profile"),
    path("following", views.following_posts_view, name="following_posts"),
    path("edit", views.edit_post_view, name="edit")
]
