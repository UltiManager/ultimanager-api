import requests
from django.contrib.auth import get_user_model
from email_auth.models import EmailVerification, EmailAddress
from rest_framework import status


def test_verify_email(live_server):
    """
    Sending a ``POST`` request to the verification endpoint with a valid
    verification token should verify the associated email address.
    """
    user = get_user_model().objects.create_user(name="Test User")
    email = EmailAddress.objects.create(address="test@example.com", user=user)
    verification = EmailVerification.objects.create(email=email)

    url = f"{live_server}/accounts/email-verifications/"
    response = requests.post(url, {"token": verification.token})

    assert response.status_code == status.HTTP_201_CREATED

    email.refresh_from_db()

    assert email.is_verified
    assert not email.verifications.exists()
