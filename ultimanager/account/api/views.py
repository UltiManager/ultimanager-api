from rest_framework import generics

from account.api import serializers


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
