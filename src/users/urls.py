from users import views

from django.urls import re_path

app_name = "users"
urlpatterns = [
    re_path(r"users/register", views.UsersAPIView.as_view({"post": "register"}), name="user-register"),
    re_path(r"users/token", views.UsersAPIView.as_view({"post": "get_token"}), name="user-token"),
    re_path(r"users/me", views.AuthenticatedUsersAPIView.as_view({"get": "retrieve", "delete": "delete"}), name="authenticated-user"),
]