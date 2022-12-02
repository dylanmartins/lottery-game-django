from django.urls import path

from users import views

from django.urls import include, re_path
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.trailing_slash = "/?"

app_name = "users"
urlpatterns = [
    re_path(r"^", include(router.urls)),
    re_path(r"^sign-in", views.UsersAPIView.as_view({"post": "sign_in"}), name="user-sign-in"),
    re_path(r"^test", views.UsersAPIView.as_view({"get": "test"}), name="user-test"),
]