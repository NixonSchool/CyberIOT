from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ForumModerationAppConfig(AppConfig):
    label = 'forum_moderation'
    name = 'machina.apps.forum_moderation'
    verbose_name = _('Machina: Forum moderation')
