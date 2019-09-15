from rest_framework import generics

from account.api import serializers


class UserCreateView(generics.CreateAPIView):
    """
    post:
    Register a new user.
    """

    serializer_class = serializers.UserCreationSerializer
