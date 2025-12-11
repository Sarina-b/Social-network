from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createPost", views.create_post, name="create_post"),
    path('profile_<str:username>', views.profile, name="profile"),
    path('user_info', views.user_info, name="user_info")
]
