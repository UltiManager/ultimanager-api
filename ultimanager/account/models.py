import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _

from account import managers


class User(PermissionsMixin, AbstractBaseUser):
    """
    A single user's account.
    """

    REQUIRED_FIELDS = ("name",)
    USERNAME_FIELD = "email"

    email = models.EmailField(
        help_text=_(
            "The user's email address. Used for logging in and receiving "
            "communications."
        ),
        unique=True,
        verbose_name=_("email address"),
    )
    id = models.UUIDField(
        default=uuid.uuid4,
        help_text=_("A unique identifier for the user."),
        primary_key=True,
        verbose_name=_("ID"),
    )
    is_active = models.BooleanField(
        default=True,
        help_text=_(
            "A boolean indicating if the user account is active and permitted "
            "to log in."
        ),
        verbose_name=_("is active"),
    )
    is_staff = models.BooleanField(
        default=False,
        help_text=_(
            "A boolean indicating if the user is permitted to access the "
            "staff interface."
        ),
        verbose_name=_("is staff"),
    )
    is_superuser = models.BooleanField(
        default=False,
        help_text=_(
            "A boolean indicating if the user should be granted all "
            "permissions even if they are not explicitly assigned."
        ),
        verbose_name=_("is superuser"),
    )
    name = models.CharField(
        help_text=_("A publicly displayed name for the user."),
        max_length=100,
        verbose_name=_("name"),
    )
    time_created = models.DateTimeField(
        auto_now_add=True,
        help_text=_("The time and date of the account's creation."),
        verbose_name=_("creation time"),
    )
    time_updated = models.DateTimeField(
        auto_now=True,
        help_text=_("The date and time of the last update to the user."),
        verbose_name=_("last update"),
    )

    objects = managers.UserManager()

    class Meta:
        ordering = ("time_created",)
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __repr__(self):
        """
        Returns:
            A string used to identify the user instance so it can be
            found again. This is primarily for debugging purposes.
        """
        return f"<account.User: id={repr(self.pk)} name={repr(self.name)}>"

    def __str__(self):
        """
        Returns:
            The user's name.
        """
        return self.name

    def get_full_name(self):
        """
        Returns:
            The user's full name.
        """
        return self.name

    def get_short_name(self):
        """
        Returns:
            The user's full name.
        """
        return self.name
