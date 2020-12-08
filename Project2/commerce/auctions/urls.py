from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("new", views.new_listing,name="new_listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("<str:category>", views.category, name="category")
]

# items = ['Games', 'Food']

# for item in items:
#     urlpatterns.append(path(f"<str:{item}>",views.category, name="category"))