import pytest
from rest_framework.test import APIClient
import copy

from users.models import User


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.fixture
def valid_create_user_payload():
    return {
        "first_name": "Test",
        "last_name": "User",
        "email": "test@gmail.com",
        "password": "my_pass",
        "confirm_password": "my_pass"
    }

@pytest.fixture
def valid_user(valid_create_user_payload):
    payload = copy.copy(valid_create_user_payload)
    payload.pop("confirm_password")
    return User.objects.create(
        **payload
    )


@pytest.fixture
def valid_user_b(valid_create_user_payload):
    payload = copy.copy(valid_create_user_payload)
    payload.pop("confirm_password", None)
    payload["email"] = "test_B@gmail.com"
    payload["username"] = "another mock.userB"
    return User.objects.create(
        **payload
    )
