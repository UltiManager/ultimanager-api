from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AccountAPIConfig(AppConfig):
    name = "account.api"
    verbose_name = _("Account Management API")
