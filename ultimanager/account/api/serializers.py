from django.contrib.auth import password_validation
from django.utils.translation import ugettext_lazy as _
from email_auth.models import EmailAddress, TOKEN_LENGTH, EmailVerification
from rest_framework import serializers

from account import models


class EmailVerificationSerializer(serializers.Serializer):
    """
    Serializer for verifying email addresses.
    """

    token = serializers.CharField(max_length=TOKEN_LENGTH, write_only=True)

    _verification: EmailVerification = None

    def save(self, **kwargs):
        """
        Mark the email address associated with the token as verified and
        delete the verification token.
        """
        self._verification.verify()

    def validate_token(self, token):
        """
        Validate the provided token.

        Args:
            token:
                The token to validate.

        Returns:
            The provided token if it exists in the database.

        Raises:
            serializers.ValidationError:
                If the token is invalid.
        """
        try:
            self._verification = EmailVerification.objects.get(token=token)
        except EmailVerification.DoesNotExist:
            raise serializers.ValidationError(
                _("The provided verification token is invalid.")
            )

        return token


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
