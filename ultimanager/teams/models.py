from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import SlugModel


class Team(SlugModel):
    """
    A team represents an organization that participates in one or more
    seasons of play.
    """

    description = models.TextField(
        blank=True,
        help_text=_("Any additional notes about the team."),
        verbose_name=_("description"),
    )
    name = models.CharField(
        help_text=_("The name of the team."),
        max_length=100,
        verbose_name=_("name"),
    )

    class Meta(SlugModel.Meta):
        ordering = ("-time_created",)
        verbose_name = _("team")
        verbose_name_plural = _("teams")

    def __repr__(self):
        """
        Returns:
            A string that unambiguously describes the team. Intended to
            be used for debugging and logging.
        """
        return (
            f"<teams.Team: id={repr(self.pk)} name={repr(self.name)} "
            f"slug={repr(self.slug)}>"
        )

    def __str__(self):
        """
        Returns:
            The team's name.
        """
        return self.name
