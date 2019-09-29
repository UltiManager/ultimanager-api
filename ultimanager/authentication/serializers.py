from django.contrib.auth import authenticate, login
from django.utils.translation import ugettext as _
from rest_framework import serializers


class SessionCreationSerializer(serializers.Serializer):
    """
    Serializer to create a new session for a user.
    """

    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"}, write_only=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "request" not in kwargs.get("context", {}):
            raise ValueError("The serializer expects a 'request' as context.")

        self._user = None

    def save(self, **kwargs):
        """
        Create a new session for the requesting user.
        """
        login(self.context["request"], self._user)

    def validate(self, attrs):
        """
        Ensure the user provided a valid email/password combination.

        Args:
            attrs:
                The attributes to validate.

        Returns:
            The validated data.
        """
        self._user = authenticate(
            self.context["request"],
            password=attrs["password"],
            username=attrs["email"],
        )

        if self._user is None:
            raise serializers.ValidationError(_("Invalid email or password."))

        return attrs
