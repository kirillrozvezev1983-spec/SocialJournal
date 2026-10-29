from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("interesting/", views.interesting, name="interesting"),
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("cabinet/", views.cabinet, name="cabinet"),
    path("post/<int:post_id>/edit/", views.edit_post, name="edit_post"),
    path("post/<int:post_id>/delete/", views.delete_post, name="delete_post"),
    path("post/<int:post_id>/like/", views.toggle_like, name="toggle_like"),
    path("user/<str:username>/", views.guest_room, name="guest_room"),
]
