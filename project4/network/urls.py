
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("post", views.post),
    path("post/<int:page_number>", views.post),
    path("user/<str:username>", views.user, name="user"),
    path("user_profile/<str:username>", views.user_profile, name="profile"),
    path("user_profile/<str:username>/<int:page_number>", views.user_profile, name="profile"),
    path("following", views.following, name='following'),
    path('following_post/<int:page_number>', views.following_post, name='following_post')
]
