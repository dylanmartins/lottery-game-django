import pytest
from django.urls import reverse

from users.models import User


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_create_user_api__success(api_client, valid_create_user_payload):

    assert len(User.objects.all()) == 0

    response = api_client.post(reverse("users:user-register"), data=valid_create_user_payload)
    assert response.status_code == 201
    assert response.data.get("access_token").startswith("Bearer")

    assert len(User.objects.all()) == 1


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_create_user_api__fails_email_already_exists(api_client, valid_user, valid_create_user_payload):

    assert len(User.objects.all()) == 1
    assert valid_create_user_payload["email"] == valid_user.email

    response = api_client.post(reverse("users:user-register"), data=valid_create_user_payload)
    assert response.status_code == 400
    assert str(response.data["email"][0]) == "user with this Email address already exists."

    assert len(User.objects.all()) == 1


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_create_user_api__should_not_create_super_user(api_client, valid_create_user_payload):

    assert len(User.objects.all()) == 0

    valid_create_user_payload["is_staff"] = True
    response = api_client.post(reverse("users:user-register"), data=valid_create_user_payload)
    assert response.status_code == 201
    assert response.data.get("access_token").startswith("Bearer")

    assert len(User.objects.all()) == 1
    user = User.objects.first()
    assert user.is_staff is False


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_create_user_api__fails_if_wrong_confirm_password(api_client, valid_create_user_payload):
    valid_create_user_payload["confirm_password"] = "wrong_password"

    assert len(User.objects.all()) == 0

    response = api_client.post(reverse("users:user-register"), data=valid_create_user_payload)
    assert response.status_code == 500
    assert response.data["detail"] == "Passwords do not match"


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_get_user_api__success(api_client, valid_user):

    assert len(User.objects.all()) == 1

    # first we generate the access token
    token = valid_user.generate_access_token()
    # and then we send it as a header
    api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    response = api_client.get(reverse("users:authenticated-user"))
    assert response.status_code == 200

    data = response.data
    assert data.get("uuid") == str(valid_user.uuid)
    assert data.get("first_name") == valid_user.first_name
    assert data.get("last_name") == valid_user.last_name
    assert data.get("email") == valid_user.email


@pytest.mark.parametrize(
    "invalid_token, expected_status_code", [
        ("Bearer invalid", 400),
        ("Bearer", 400),
        (None, 403),
        ("invalid", 403),
        (182, 403),
    ]
)
@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_get_user_api__fails_invalid_token(api_client, valid_user, invalid_token, expected_status_code):

    assert len(User.objects.all()) == 1

    # and then we send it as a cookie
    api_client.credentials(HTTP_AUTHORIZATION=invalid_token)

    response = api_client.get(reverse("users:authenticated-user"))
    assert response.status_code == expected_status_code


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_delete_user_api__success(api_client, valid_user):

    assert len(User.objects.all()) == 1

    # first we generate the access token
    token = valid_user.generate_access_token()
    # and then we send it as a header
    api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    response = api_client.delete(reverse("users:authenticated-user"))
    assert response.status_code == 202
    assert response.data["message"] == "Delete requested successfully"

    assert len(User.objects.all()) == 0
