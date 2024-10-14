"""
Forum Permission Model Admin Definitions
========================================

This module defines admin classes that are used to configure and display the forum permission
models in the Django administration dashboard. These classes facilitate the management of
forum permissions for users and groups.

"""

from django.contrib import admin
from machina.core.db.models import get_model

# Retrieve the forum permission models from the database
ForumPermission = get_model('forum_permission', 'ForumPermission')
GroupForumPermission = get_model('forum_permission', 'GroupForumPermission')
UserForumPermission = get_model('forum_permission', 'UserForumPermission')


class ForumPermissionAdmin(admin.ModelAdmin):
    """ Admin interface for managing Forum Permissions. """

    search_fields = ('codename', )  # Fields that can be searched in the admin interface
    list_display = ('name', 'codename', )  # Columns displayed in the list view


class GroupForumPermissionAdmin(admin.ModelAdmin):
    """ Admin interface for managing Group Forum Permissions. """

    search_fields = ('permission__codename', 'group__name', )  # Searchable fields
    list_display = ('group', 'forum', 'permission', 'has_perm', )  # Columns displayed in the list view
    list_editables = ('has_perm', )  # Fields that can be edited directly in the list view
    raw_id_fields = ('group', )  # Use a raw ID widget for group selection
    list_filter = ['forum', 'group']  # Filters available in the sidebar


class UserForumPermissionAdmin(admin.ModelAdmin):
    """ Admin interface for managing User Forum Permissions. """

    search_fields = ('permission__codename', 'user__username', )  # Searchable fields
    list_display = (
        'user',
        'anonymous_user',
        'authenticated_user',
        'forum',
        'permission',
        'has_perm',
    )  # Columns displayed in the list view
    list_editables = ('has_perm', )  # Fields that can be edited directly in the list view
    raw_id_fields = ('user', )  # Use a raw ID widget for user selection
    list_filter = ['forum']  # Filters available in the sidebar


# Register the admin classes with the associated models
admin.site.register(ForumPermission, ForumPermissionAdmin)
admin.site.register(GroupForumPermission, GroupForumPermissionAdmin)
admin.site.register(UserForumPermission, UserForumPermissionAdmin)
