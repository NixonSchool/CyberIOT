from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ForumMemberAppConfig(AppConfig):
    label = 'forum_member'
    name = 'machina.apps.forum_member'
    verbose_name = _('Machina: Forum members')

    def ready(self):
        from . import receivers  # noqa: F401
