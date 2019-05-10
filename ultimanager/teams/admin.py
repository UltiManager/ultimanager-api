from django.contrib import admin

from teams import models


@admin.register(models.Team)
class TeamAdmin(admin.ModelAdmin):
    """
    Admin for the :py:class:`Team` model.
    """

    fields = ("name", "slug", "time_created", "time_updated", "description")
    list_display = ("name", "time_created", "time_updated")
    readonly_fields = ("slug", "time_created", "time_updated")
    search_fields = ("name",)
