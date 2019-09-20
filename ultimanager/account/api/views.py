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


class UserCreateView(generics.CreateAPIView):
    """
    post:
    Register a new user.
    """

    serializer_class = serializers.UserCreationSerializer
