"""

The provided code defines a `ForumPermissionChecker` class that manages
and checks user permissions for forum-related actions within a Django application.
It initializes with a user object and caches the forum permissions to optimize
repeated checks. The main functionality includes determining if a user has
specific permissions (like posting) based on their authentication status,
superuser status, and specific permissions associated with forums. If the user is
not logged in or inactive, permission checks are bypassed. The class also fetches
permissions for both individual users and their associated groups, ensuring that
permissions are processed based on various criteria, such as whether they apply
globally or to specific forums.

In the `get_perms_for_forumlist` method, the code filters and categorizes
permissions into granted and non-granted sets for users, groups, and all users,
based on their context (e.g., whether they belong to a forum or are granted
permissions globally). This involves querying the database for relevant permission
records and performing logical checks to determine which permissions to grant or
deny. Ultimately, the method compiles a comprehensive set of permission codes for
each forum, considering both direct user permissions and those granted through
groups or globally, returning an organized mapping of forums to permissions.
This ensures a robust and flexible permission system that can accommodate various
user roles and contexts within the forum environment.

"""
from django.contrib.auth import get_user_model
from django.db.models import Q
from machina.conf import settings as machina_settings
from machina.core.db.models import get_model

ForumPermission = get_model('forum_permission', 'ForumPermission')
GroupForumPermission = get_model('forum_permission', 'GroupForumPermission')
UserForumPermission = get_model('forum_permission', 'UserForumPermission')


class ForumPermissionChecker:
    def __init__(self, user):
        self.user = user
        self._forum_perms_cache = {}

    def has_perm(self, perm, forum):
        if self.user.is_superuser or self.user.is_staff:
            return True
        if self.user.is_anonymous:
            return perm in ['can_see_forum', 'can_read_forum']
        return perm in self.get_perms(forum)

    def get_perms(self, forum):
        if not self.user.is_active:
            return []

        forum_identifier = 'global' if forum is None else forum.id
        if forum_identifier not in self._forum_perms_cache:
            if self.user.is_superuser or self.user.is_staff:
                permcodes = list(ForumPermission.objects.values_list('codename', flat=True))
            elif self.user.is_anonymous:
                permcodes = ['can_see_forum', 'can_read_forum']
            else:
                perms = self.get_perms_for_forumlist([forum])
                permcodes = perms[forum]
            self._forum_perms_cache[forum_identifier] = permcodes
        return self._forum_perms_cache[forum_identifier]

    def get_perms_for_forumlist(self, forums):
        if self.user.is_superuser or self.user.is_staff:
            return {forum: list(ForumPermission.objects.values_list('codename', flat=True)) for forum in forums}

        if self.user.is_anonymous:
            return {forum: ['can_see_forum', 'can_read_forum'] for forum in forums}

        user_perms = (
            UserForumPermission.objects.select_related()
            .filter(Q(forum__isnull=True) | Q(forum__in=forums))
            .filter(user=self.user)
        )

        group_perms = (
            GroupForumPermission.objects.select_related()
            .filter(Q(forum__isnull=True) | Q(forum__in=forums))
            .filter(group__in=self.user.groups.all())
        )

        all_perms = list(user_perms) + list(group_perms)

        forum_permissions = {}
        for forum in forums:
            forum_permissions[forum] = (
                    ['can_see_forum', 'can_read_forum'] +
                    [perm.permission.codename for perm in all_perms if
                     perm.has_perm and (perm.forum is None or perm.forum == forum)] +
                    ['can_post_without_approval', 'can_edit_own_posts', 'can_delete_own_posts']
            )

        return forum_permissions

    def admin_perm_string(self, model_perm):
        return 'forum.{}'.format(model_perm)