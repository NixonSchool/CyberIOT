"""

The provided code defines abstract models for managing forum permissions in a
Django application, specifically within the `forum_permission` app. It includes
the `AbstractForumPermission` class, which establishes a structure for forum
permissions identified by unique codenames, along with methods to retrieve their
display names. The `BaseAuthForumPermission` class extends this to incorporate
authentication status, allowing permissions to be associated with specific forums.

The `AbstractUserForumPermission` model adds user-specific permission management,
ensuring that permissions can target individual users, anonymous users, or all
authenticated users, while enforcing uniqueness across user and forum combinations.
Lastly, the `AbstractGroupForumPermission` model similarly manages permissions
for user groups, establishing relationships between permissions, forums, and
groups, thereby facilitating flexible and scalable permission management within
the forum system.


"""
from django.conf import settings
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from machina.core.loading import get_class

PermissionConfig = get_class('forum_permission.defaults', 'PermissionConfig')


class AbstractForumPermission(models.Model):
    codename = models.CharField(
        max_length=150, verbose_name=_('Permission codename'), unique=True, db_index=True,
    )

    class Meta:
        abstract = True
        app_label = 'forum_permission'
        verbose_name = _('Forum permission')
        verbose_name_plural = _('Forum permissions')

    def __str__(self):
        return '{} - {}'.format(self.codename, self.name)

    @cached_property
    def name(self):
        perm_config = PermissionConfig().get(self.codename)
        return perm_config['label'] if perm_config else None


class BaseAuthForumPermission(models.Model):
    permission = models.ForeignKey(
        'forum_permission.ForumPermission', on_delete=models.CASCADE,
        verbose_name=_('Forum permission'),
    )
    has_perm = models.BooleanField(verbose_name=_('Has permission'), default=True, db_index=True)
    forum = models.ForeignKey(
        'forum.Forum', blank=True, null=True, on_delete=models.CASCADE, verbose_name=_('Forum'),
    )

    class Meta:
        abstract = True


class AbstractUserForumPermission(BaseAuthForumPermission):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE,
        verbose_name=_('User'),
    )
    anonymous_user = models.BooleanField(
        verbose_name=_('Target anonymous user'), default=False, db_index=True,
    )
    authenticated_user = models.BooleanField(
        verbose_name=_('Target any logged in user'), default=False, db_index=True,
    )

    class Meta:
        abstract = True
        unique_together = ('permission', 'forum', 'user',)
        app_label = 'forum_permission'
        verbose_name = _('User forum permission')
        verbose_name_plural = _('User forum permissions')

    def __str__(self):
        if self.forum:
            return '{} - {} - {}'.format(self.permission, self.user, self.forum)
        return '{} - {}'.format(self.permission, self.user)

    def clean(self):
        super().clean()
        if (
                (self.user is None and not self.anonymous_user and not self.authenticated_user) or
                ((self.user and self.anonymous_user) or (self.user and self.authenticated_user) or
                 (self.anonymous_user and self.authenticated_user))
        ):
            raise ValidationError(
                _(
                    "A permission should target either a specific user, an anonymous user " +
                    "or any authenticated user."
                ),
            )


class AbstractGroupForumPermission(BaseAuthForumPermission):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name=_('Group'))

    class Meta:
        abstract = True
        unique_together = ('permission', 'forum', 'group',)
        app_label = 'forum_permission'
        verbose_name = _('Group forum permission')
        verbose_name_plural = _('Group forum permissions')

    def __str__(self):
        if self.forum:
            return '{} - {} - {}'.format(self.permission, self.group, self.forum)
        return '{} - {}'.format(self.permission, self.group)
