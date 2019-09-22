from rest_framework import generics

from account.api import serializers


class EmailVerificationRequestView(generics.CreateAPIView):
    """
    post:
    Request a new verification token for a specific email address.

    If the provided email address exists in the database, a new
    verification token will be sent to the address. In any other case, a
    notification message will be sent to the user prompting them with
    the appropriate actions.
    """

    serializer_class = serializers.EmailVerificationRequestSerializer


class EmailVerificationView(generics.CreateAPIView):
    """
    post:
    Verify an email address using a verification token.
    """

    serializer_class = serializers.EmailVerificationSerializer


class PasswordResetRequestView(generics.CreateAPIView):
    """
    post:
    Send a token to the provided email address that the user can use to
    reset their password.

    If the provided email address has not been verified or has not been
    registered with our system, no email is sent.
    """

    serializer_class = serializers.PasswordResetRequestSerializer


class PasswordResetView(generics.CreateAPIView):
    """
    post:
    Reset the user's password using a valid password reset token to
    authorize the operation.
    """

    serializer_class = serializers.PasswordResetSerializer


class UserCreateView(generics.CreateAPIView):
    """
    post:
    Register a new user.
    """

    serializer_class = serializers.UserCreationSerializer
