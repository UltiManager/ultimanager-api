from unittest import mock

from email_auth.models import EmailAddress

from account.api import serializers


# Since the serializer uses Django's password validation, we actually
# need a "strong" password for testing.
PASSWORD = "MySup3rSecurePassword"


@mock.patch(
    "email_auth.models.EmailAddress.send_verification_email", autospec=True
)
def test_save_with_valid_data_should_send_verification_email(_, db):
    """
    Saving the serializer with valid data should create a new user and
    send them a verification email.
    """
    data = {
        "email": "test@example.com",
        "name": "Test User",
        "password": PASSWORD,
    }
    serializer = serializers.UserCreationSerializer(data=data)

    assert serializer.is_valid()
    user = serializer.save()

    assert serializer.data == {"email": data["email"], "name": data["name"]}
    assert user.name == data["name"]
    assert user.check_password(data["password"])

    email = user.email_addresses.get()
    assert email.address == data["email"]
    assert email.send_verification_email.call_count == 1


@mock.patch(
    "email_auth.models.EmailAddress.send_duplicate_notification", autospec=True
)
def test_save_with_already_registered_email(_, mock_email_address_qs):
    """
    Saving the serializer with an email address that has already been
    registered should send a notification to the email address.
    """
    email = EmailAddress(address="test@example.com")

    filter_result = mock.Mock()
    filter_result.exists.return_value = True
    filter_result.get.return_value = email
    mock_email_address_qs.filter.return_value = filter_result

    data = {"email": email.address, "name": "Test User", "password": PASSWORD}
    serializer = serializers.UserCreationSerializer(data=data)

    assert serializer.is_valid()
    user = serializer.save()

    assert user is None
    assert mock_email_address_qs.filter.call_args[1] == {
        "address__iexact": data["email"]
    }
    assert email.send_duplicate_notification.call_count == 1


@mock.patch(
    "account.api.serializers.password_validation.validate_password",
    autospec=True,
)
def test_validate_password(mock_validate_password):
    """
    Passwords should be run through Django's password validation system.
    """
    password = "password"
    serializer = serializers.UserCreationSerializer()

    result = serializer.validate_password(password)

    assert result == password
    assert mock_validate_password.call_args[0] == (password,)
