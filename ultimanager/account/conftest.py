from unittest import mock

import pytest
from email_auth.models import EmailAddress


@pytest.fixture
def mock_email_address_qs():
    mock_qs = mock.Mock(spec=EmailAddress.objects)
    mock_qs.all.return_value = mock_qs

    with mock.patch("email_auth.models.EmailAddress.objects", new=mock_qs):
        yield mock_qs
