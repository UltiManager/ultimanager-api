import requests
from django.contrib.auth import get_user_model
from email_auth.models import EmailAddress, PasswordReset
from rest_framework import status


def test_password_reset_unregistered_email(live_server, mailoutbox):
    """
    Submitting a password reset request for a non-existent email should
    do nothing.
    """
    data = {"email": "does-not-exist@example.com"}
    url = f"{live_server}/accounts/password-reset-requests/"
    response = requests.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == data
    assert len(mailoutbox) == 0


def test_password_reset_verified_email(live_server, mailoutbox):
    """
    Submitting a password reset request with a verified email should
    send a new password reset token to the provided address.
    """
    user = get_user_model().objects.create_user(name="Test User")
    email = EmailAddress.objects.create(
        address="test@example.com", is_verified=True, user=user
    )
    data = {"email": email.address}
    url = f"{live_server}/accounts/password-reset-requests/"
    response = requests.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == data

    msg = mailoutbox[0]
    reset = PasswordReset.objects.get()

    assert msg.to == [email.address]
    assert reset.token in msg.body
