"""

This function retrieves the display name of a forum member using the
configured method.

"""
from machina.conf import settings as machina_settings


def get_forum_member_display_name(user):
    return getattr(user, machina_settings.USER_DISPLAY_NAME_METHOD)()
