from django.urls import path

from users import views

from django.urls import include, re_path
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.trailing_slash = "/?"

app_name = "users"
urlpatterns = [
    re_path(r"^", include(router.urls)),
    re_path(r"register", views.UsersAPIView.as_view({"post": "register"}), name="user-register"),
    re_path(r"token", views.UsersAPIView.as_view({"post": "get_token"}), name="user-token"),
    re_path(r"me", views.AuthenticatedUsersAPIView.as_view({"get": "retrieve"}), name="user-retrieve"),
]