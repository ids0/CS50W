from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/random", views.random_entry, name="random"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("new", views.new, name="new"),
    path("wiki/<str:title>/edit", views.edit, name="edit"),

]
