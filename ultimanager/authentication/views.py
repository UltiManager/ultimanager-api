from rest_framework import generics

from authentication import serializers


class SessionCreationView(generics.CreateAPIView):
    """
    post:
    Create a new session for a user.

    The session uses cookies to authenticate the user's requests.
    """

    serializer_class = serializers.SessionCreationSerializer
