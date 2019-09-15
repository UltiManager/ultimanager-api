from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _

from account import managers
from core.models import BaseModel


class User(PermissionsMixin, AbstractBaseUser, BaseModel):
    """
    A single user's account.
    """

    NAME_LENGTH = 100
    USERNAME_FIELD = "name"

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
        max_length=NAME_LENGTH,
        verbose_name=_("name"),
    )

    objects = managers.UserManager()

    class Meta(BaseModel.Meta):
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
