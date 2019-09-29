import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from email_auth.models import EmailAddress
from rest_framework import status


def test_create_session(live_server):
    """
    Users should be able to create a session with a valid email/password
    combination.
    """
    password = "password"
    user = get_user_model().objects.create_user(
        name="Test User", password=password
    )
    email = EmailAddress.objects.create(
        address="test@example.com", is_verified=True, user=user
    )

    data = {"email": email.address, "password": password}
    url = f"{live_server}/authentication/sessions/"
    response = requests.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.cookies[settings.SESSION_COOKIE_NAME]
