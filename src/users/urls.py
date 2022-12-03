from django.urls import re_path

from users import views


app_name = "users"
urlpatterns = [
    re_path(
        r"users/register",
        views.UsersRegisterAPIView.as_view({"post": "register"}),
        name="user-register",
    ),
    re_path(
        r"users/token",
        views.UsersTokenAPIView.as_view({"post": "get_token"}),
        name="user-token",
    ),
    re_path(
        r"users/me",
        views.AuthenticatedUsersAPIView.as_view({"get": "retrieve", "delete": "delete"}),
        name="authenticated-user",
    ),
]
