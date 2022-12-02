import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication


class JWTAuthentication(BaseAuthentication):

    def authenticate(self, request):
        auth = request.headers.get("Authorization", "")
        if not isinstance(auth, str) or not auth.startswith("Bearer"):
            return None

        jwt_token = auth.split("Bearer")[1].strip()
        try:
            payload = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("unauthenticated")
        except Exception:
            # If any other exception happens we return an error 400
            raise exceptions.ValidationError

        user = get_user_model().objects.filter(uuid=payload["user_uuid"]).first()

        if user is None:
            raise exceptions.AuthenticationFailed("User not found!")

        return (user, None)
