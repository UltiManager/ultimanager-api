import requests
from django.contrib.auth import get_user_model
from email_auth.models import EmailAddress, EmailVerification
from rest_framework import status


def test_create_email_verification_request(live_server, mailoutbox):
    """
    A user should be able to resend the verification email for an email
    they have not yet verified.
    """
    user = get_user_model().objects.create_user(name="Test User")
    email = EmailAddress.objects.create(address="test@example.com", user=user)

    data = {"email": email.address}
    url = f"{live_server}/accounts/email-verification-requests/"
    response = requests.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == data

    verification = EmailVerification.objects.get()
    msg = mailoutbox[0]

    assert "Verify" in msg.subject
    assert msg.to == [email.address]
    assert verification.token in msg.body
