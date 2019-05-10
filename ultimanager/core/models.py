import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _


class BaseModel(models.Model):
    """
    A base model with common attributes shared across models.
    """

    id = models.UUIDField(
        default=uuid.uuid4,
        help_text=_("A unique identifier for the instance."),
        primary_key=True,
        verbose_name=_("ID"),
    )
    time_created = models.DateTimeField(
        auto_now_add=True,
        help_text=_("The date and time of the object's creation."),
        verbose_name=_("creation time"),
    )
    time_updated = models.DateTimeField(
        auto_now=True,
        help_text=_(
            "The date and time of the last update made to the object."
        ),
        verbose_name=_("last update time"),
    )

    class Meta:
        abstract = True


class SlugModel(BaseModel):
    """
    Mixin that generates a slug for the instance.
    """

    SLUG_ID_LENGTH = 6
    SLUG_LENGTH = 50
    SLUG_SOURCE = "name"
    # Length of slugified text must leave room for the random slug ID
    # and a separator character (eg '-').
    SLUG_TEXT_LENGTH = SLUG_LENGTH - SLUG_ID_LENGTH - 1

    slug = models.SlugField(
        help_text=_(
            "A unique identifier for the instance derived from the name of "
            "the instance."
        ),
        max_length=SLUG_LENGTH,
        verbose_name=_("slug"),
    )

    class Meta(BaseModel.Meta):
        abstract = True
