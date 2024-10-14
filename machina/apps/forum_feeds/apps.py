from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ForumFeedsAppConfig(AppConfig):
    label = 'forum_feeds'
    name = 'machina.apps.forum_feeds'
    verbose_name = _('Machina: Forum feeds')
