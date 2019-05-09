from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _

from account import models


@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    """
    Admin for the :py:class:`User` model.
    """

    add_fieldsets = (
        (None, {"fields": ("email", "name", "password1", "password2")}),
    )
    date_hierarchy = "time_created"
    fieldsets = (
        (_("Personal Information"), {"fields": ("email", "name", "password")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            _("Time Information"),
            {
                "classes": ("collapse",),
                "fields": ("time_created", "time_updated"),
            },
        ),
    )
    list_display = (
        "email",
        "name",
        "is_active",
        "is_staff",
        "is_superuser",
        "time_created",
        "time_updated",
    )
    ordering = ("time_created",)
    readonly_fields = ("time_created", "time_updated")
    search_fields = ("email", "name")
