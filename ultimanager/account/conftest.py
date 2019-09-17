from unittest import mock

import pytest
from email_auth.models import EmailAddress, EmailVerification


@pytest.fixture
def mock_email_address_qs():
    mock_qs = mock.Mock(spec=EmailAddress.objects)
    mock_qs.all.return_value = mock_qs

    with mock.patch("email_auth.models.EmailAddress.objects", new=mock_qs):
        yield mock_qs


@pytest.fixture
def mock_email_verification_qs():
    mock_qs = mock.Mock(spec=EmailVerification.objects)
    mock_qs.all.return_value = mock_qs

    with mock.patch(
        "email_auth.models.EmailVerification.objects", new=mock_qs
    ):
        yield mock_qs
