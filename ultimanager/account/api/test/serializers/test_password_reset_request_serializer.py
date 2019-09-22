from unittest import mock

from email_auth.models import EmailAddress

from account.api import serializers


def return_for_conditions(obj, raise_ex=False, **kwargs):
    def handler(**inner_kwargs):
        if kwargs.items() <= inner_kwargs.items():
            if raise_ex:
                raise obj

            return obj

    return handler


def test_save_unregistered_email(mock_email_address_qs):
    """
    If the provided email address doesn't exist in the system, saving
    should do nothing.
    """
    address = "test@example.com"
    mock_email_address_qs.get.side_effect = return_for_conditions(
        EmailAddress.DoesNotExist, address__iexact=address, raise_ex=True
    )

    data = {"email": address}
    serializer = serializers.PasswordResetRequestSerializer(data=data)

    assert serializer.is_valid()
    result = serializer.save()

    assert result is None
    assert serializer.data == data


def test_save_unverified_email(mock_email_address_qs):
    """
    If the provided email address has not been verified yet, saving the
    serializer should do nothing.
    """
    address = "test@example.com"
    mock_email_address_qs.get.side_effect = return_for_conditions(
        EmailAddress.DoesNotExist,
        address__iexact=address,
        is_verified=True,
        raise_ex=True,
    )

    data = {"email": address}
    serializer = serializers.PasswordResetRequestSerializer(data=data)

    assert serializer.is_valid()
    result = serializer.save()

    assert result is None
    assert serializer.data == data


@mock.patch("email_auth.models.PasswordReset.send_email")
def test_save_verified_email(_, mock_email_address_qs):
    """
    If a verified email is provided, saving the serializer should send
    a new password reset token to the provided address.
    """
    email = EmailAddress(address="test@example.com")
    mock_email_address_qs.get.side_effect = return_for_conditions(
        email, address__iexact=True, is_verified=True
    )

    data = {"email": email.address}
    serializer = serializers.PasswordResetRequestSerializer(data=data)

    assert serializer.is_valid()
    result = serializer.save()

    assert serializer.data == data
    assert result.send_email.call_count == 1
