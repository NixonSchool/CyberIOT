import datetime as dt
from functools import reduce
from django.db import models
from django.utils.timezone import now
from mptt.utils import get_cached_trees
from machina.core.db.models import get_model
from machina.core.loading import get_class
from django.db import models

Forum = get_model('forum', 'Forum')
GroupForumPermission = get_model('forum_permission', 'GroupForumPermission')
Post = get_model('forum_conversation', 'Post')
TopicPollVote = get_model('forum_polls', 'TopicPollVote')
UserForumPermission = get_model('forum_permission', 'UserForumPermission')
ForumPermissionChecker = get_class('forum_permission.checker', 'ForumPermissionChecker')
get_anonymous_user_forum_key = get_class(
    'forum_permission.shortcuts', 'get_anonymous_user_forum_key')


class PermissionHandler:
    def __init__(self):
        self._granted_forums_cache = {}
        self._forum_ancestors_cache = {}
        self._user_perm_checkers_cache = {}

    def forum_list_filter(self, qs, user):
        checker = self._get_checker(user)
        return [forum for forum in qs if checker.has_perm('can_see_forum', forum)]

    def get_readable_forums(self, forums, user):
        checker = self._get_checker(user)
        return [forum for forum in forums if checker.has_perm('can_read_forum', forum)]

    def can_read_forum(self, forum, user):
        return self._get_checker(user).has_perm('can_read_forum', forum)

    def can_add_topic(self, forum, user):
        return user.is_authenticated and self._get_checker(user).has_perm('can_post_without_approval', forum)

    def can_add_stickies(self, forum, user):
        return user.is_superuser or user.is_staff

    def can_add_announcements(self, forum, user):
        return user.is_superuser or user.is_staff

    def can_post_without_approval(self, forum, user):
        return user.is_authenticated and self._get_checker(user).has_perm('can_post_without_approval', forum)

    def can_add_post(self, topic, user):
        return user.is_authenticated and self._get_checker(user).has_perm('can_post_without_approval', topic.forum)

    def can_edit_post(self, post, user):
        return (user.is_authenticated and post.poster == user) or user.is_superuser or user.is_staff

    def can_delete_post(self, post, user):
        return (user.is_authenticated and post.poster == user) or user.is_superuser or user.is_staff

    def can_create_polls(self, forum, user):
        return user.is_authenticated and self._get_checker(user).has_perm('can_create_polls', forum)

    def can_vote_in_poll(self, poll, user):
        return user.is_authenticated and self._get_checker(user).has_perm('can_vote_in_poll', poll.topic.forum)

    def can_attach_files(self, forum, user):
        return user.is_authenticated and self._get_checker(user).has_perm('can_attach_file', forum)

    def can_download_files(self, forum, user):
        return self._get_checker(user).has_perm('can_download_file', forum)

    def can_subscribe_to_topic(self, topic, user):
        return user.is_authenticated and self._get_checker(user).has_perm('can_subscribe_to_topic', topic.forum)

    def can_unsubscribe_from_topic(self, topic, user):
        return user.is_authenticated

    # Moderation
    def get_moderation_queue_forums(self, user):
        return Forum.objects.all() if user.is_superuser or user.is_staff else []

    def can_access_moderation_queue(self, user):
        return user.is_superuser or user.is_staff

    def can_lock_topics(self, forum, user):
        return user.is_superuser or user.is_staff

    def can_move_topics(self, forum, user):
        return user.is_superuser or user.is_staff

    def can_delete_topics(self, forum, user):
        return user.is_superuser or user.is_staff

    def can_update_topics_to_normal_topics(self, forum, user):
        return user.is_superuser or user.is_staff

    def can_update_topics_to_sticky_topics(self, forum, user):
        return user.is_superuser or user.is_staff

    def can_update_topics_to_announces(self, forum, user):
        return user.is_superuser or user.is_staff

    def can_approve_posts(self, forum, user):
        return user.is_superuser or user.is_staff

    # Common helper methods
    def _is_post_author(self, post, user):
        return (post.poster == user) if user.is_authenticated else (
                post.anonymous_key and post.anonymous_key == get_anonymous_user_forum_key(user)
        )

    def _get_hidden_forum_ids(self, forums, user):
        return []  # No hidden forums

    def _get_forums_for_user(self, user, perm_codenames, use_tree_hierarchy=False):
        return self._get_all_forums()  # Return all forums for all users

    def _get_all_forums(self):
        return Forum.objects.all()

    def _get_checker(self, user):
        if user not in self._user_perm_checkers_cache:
            self._user_perm_checkers_cache[user] = ForumPermissionChecker(user)
        return self._user_perm_checkers_cache[user]
