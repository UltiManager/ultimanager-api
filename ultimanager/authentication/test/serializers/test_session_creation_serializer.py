from unittest import mock

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory

from authentication import serializers


def test_init_with_request():
    """
    Initializing the serializer with a request should be valid.
    """
    serializers.SessionCreationSerializer(context={"request": "foo"})


def test_init_without_request():
    """
    Initializing the serializer without the request as context should
    fail.
    """
    with pytest.raises(ValueError):
        serializers.SessionCreationSerializer()


@mock.patch("authentication.serializers.authenticate", autospec=True)
@mock.patch("authentication.serializers.login", autospec=True)
def test_save_valid_data(mock_login, mock_authenticate):
    """
    Saving a serializer with a valid email/password combination should
    create a new session for the user.
    """
    request_factory = APIRequestFactory()

    user = get_user_model()()
    mock_authenticate.return_value = user

    data = {"email": "test@example.com", "password": "password"}
    request = request_factory.post("/")
    serializer = serializers.SessionCreationSerializer(
        context={"request": request}, data=data
    )

    assert serializer.is_valid()
    serializer.save()

    assert serializer.data == {"email": data["email"]}
    assert mock_authenticate.call_args[0][0] == request
    assert mock_authenticate.call_args[1] == {
        "password": data["password"],
        "username": data["email"],
    }
    assert mock_login.call_args[0] == (request, user)


@mock.patch("authentication.serializers.authenticate", autospec=True)
def test_validate_with_valid_credentials(mock_authenticate):
    """
    If valid credentials are supplied, validation should succeed.
    """
    request_factory = APIRequestFactory()

    user = get_user_model()()
    mock_authenticate.return_value = user

    data = {"email": "test@example.com", "password": "password"}
    request = request_factory.post("/")
    serializer = serializers.SessionCreationSerializer(
        context={"request": request}, data=data
    )

    assert serializer.is_valid()


@mock.patch("authentication.serializers.authenticate", autospec=True)
def test_validate_with_invalid_credentials(mock_authenticate):
    """
    If invalid credentials are supplied, validation should not succeed.
    """
    request_factory = APIRequestFactory()

    mock_authenticate.return_value = None

    data = {"email": "test@example.com", "password": "password"}
    request = request_factory.post("/")
    serializer = serializers.SessionCreationSerializer(
        context={"request": request}, data=data
    )

    assert not serializer.is_valid()
    assert set(serializer.errors.keys()) == {"non_field_errors"}
    assert mock_authenticate.call_args[0][0] == request
    assert mock_authenticate.call_args[1] == {
        "password": data["password"],
        "username": data["email"],
    }
