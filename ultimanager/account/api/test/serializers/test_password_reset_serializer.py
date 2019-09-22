from unittest import mock


# Since the serializer uses Django's built in password validators, we
# need a password that will pass them.
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from email_auth.models import EmailAddress, PasswordReset

from account.api import test_utils, serializers

NEW_PASSWORD = "MySup3rSecurePassword"


@mock.patch("account.models.User.save", autospec=True)
@mock.patch("email_auth.models.PasswordReset.delete", autospec=True)
def test_save_valid_token(_, __, mock_password_reset_qs):
    """
    Saving the serializer with a valid token should reset the password
    of the user associated with the reset.
    """
    user = get_user_model()(name="Test User")
    email = EmailAddress(user=user)
    reset = PasswordReset(email=email)
    mock_password_reset_qs.get.side_effect = test_utils.return_for_conditions(
        reset, token=reset.token
    )

    data = {"password": NEW_PASSWORD, "token": reset.token}
    serializer = serializers.PasswordResetSerializer(data=data)

    assert serializer.is_valid()
    serializer.save()

    assert serializer.data == {}
    assert user.check_password(NEW_PASSWORD)
    assert user.save.call_count == 1
    assert reset.delete.call_count == 1


@mock.patch(
    "account.api.serializers.password_validation.validate_password",
    autospec=True,
    side_effect=ValidationError("Invalid password"),
)
def test_validate(mock_validate_password, mock_password_reset_qs):
    """
    If the provided token is valid, the provided password should be run
    through Django's password validation system.
    """
    user = get_user_model()()
    email = EmailAddress(user=user)
    reset = PasswordReset(email=email)
    mock_password_reset_qs.get.side_effect = test_utils.return_for_conditions(
        reset, token=reset.token
    )

    data = {"password": NEW_PASSWORD, "token": reset.token}
    serializer = serializers.PasswordResetSerializer(data=data)

    assert not serializer.is_valid()
    assert set(serializer.errors.keys()) == {"password"}
    assert mock_validate_password.call_args[0][0] == NEW_PASSWORD
    assert mock_validate_password.call_args[1] == {"user": user}


def test_validate_invalid_token(mock_password_reset_qs):
    """
    If the provided token is not valid, a validation error should be
    raised.
    """
    token = "foo"
    mock_password_reset_qs.get.side_effect = test_utils.return_for_conditions(
        PasswordReset.DoesNotExist, raise_ex=True, token=token
    )

    data = {"password": NEW_PASSWORD, "token": token}
    serializer = serializers.PasswordResetSerializer(data=data)

    assert not serializer.is_valid()
    assert set(serializer.errors.keys()) == {"token"}
