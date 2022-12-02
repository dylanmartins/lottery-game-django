import datetime
import uuid

import jwt
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(
        verbose_name="Email address",
        max_length=255,
        unique=True,
    )
    password = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def generate_access_token(self):
        payload = {
            "user_uuid": str(self.uuid),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            "iat": datetime.datetime.utcnow()
        }

        return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256").decode("utf-8")
