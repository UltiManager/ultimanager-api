from django.contrib.auth import password_validation
from email_auth.models import EmailAddress
from rest_framework import serializers

from account import models


class UserCreationSerializer(serializers.Serializer):

    email = serializers.EmailField(required=True)
    name = serializers.CharField(
        max_length=models.User.NAME_LENGTH, required=True
    )
    password = serializers.CharField(
        style={"input_type": "password"}, write_only=True
    )

    def save(self, **kwargs):
        """
        Create a new user and send them a verification email.

        Returns:
            The newly registered user or ``None`` if no new user is
            created.
        """
        email_query = EmailAddress.objects.filter(
            address__iexact=self.validated_data["email"]
        )

        if email_query.exists():
            email = email_query.get()
            email.send_duplicate_notification()

            return None

        user = models.User.objects.create_user(
            name=self.validated_data["name"],
            password=self.validated_data["password"],
        )
        email = EmailAddress.objects.create(
            address=self.validated_data["email"], user=user
        )
        email.send_verification_email()

        return user

    def validate_password(self, password: str) -> str:
        """
        Run the provided password through Django's password validation
        system.

        Args:
            password:
                The password to validate.

        Returns:
            The validated password.
        """
        password_validation.validate_password(password)

        return password
