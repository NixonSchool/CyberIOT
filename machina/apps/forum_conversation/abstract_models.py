"""

The code defines an abstract model for a forum topic within the forum,
encapsulating various properties and behaviors associated with topics.
It includes fields for the forum to which the topic belongs, the poster,
subject, slug, type (e.g., default, sticky, announce),
status (e.g., locked, unlocked), approval status, post counts,
view counts, and timestamps for creation and updates.
The model also manages relationships with posts and subscribers,
implements methods for validation, saving, deleting,
and updating associated statistics, ensuring that all
necessary data is maintained correctly when changes occur.

`AbstractPost` defines a model representing a forum post linked to a specific topic.
It includes fields for the post's author, content, approval status,
and metadata such as the number of updates and last updater.
The class provides methods for validation, saving, and deleting posts,
ensuring that each post maintains its relationship with the associated topic
and updates the topic's statistics accordingly. Properties are also
defined to check the post's position within the topic, such as whether
it's the first or last post.

"""
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils.encoding import force_str
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from machina.conf import settings as machina_settings
from machina.core import validators
from machina.core.loading import get_class
from machina.models.abstract_models import DatedModel
from machina.models.fields import MarkupTextField

ApprovedManager = get_class('forum_conversation.managers', 'ApprovedManager')


class AbstractTopic(models.Model):
    forum = models.ForeignKey(
        'forum.Forum', related_name='topics', on_delete=models.CASCADE,
        verbose_name=_('Topic forum'),
    )
    poster = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE,
        verbose_name=_('Poster'),
    )
    subject = models.CharField(max_length=255, verbose_name=_('Subject'))
    slug = models.SlugField(max_length=255, verbose_name=_('Slug'))
    TOPIC_POST, TOPIC_STICKY, TOPIC_ANNOUNCE = 0, 1, 2
    TYPE_CHOICES = (
        (TOPIC_POST, _('Default topic')),
        (TOPIC_STICKY, _('Sticky')),
        (TOPIC_ANNOUNCE, _('Announce')),
    )
    type = models.PositiveSmallIntegerField(
        choices=TYPE_CHOICES, db_index=True, verbose_name=_('Topic type'),
    )
    TOPIC_UNLOCKED, TOPIC_LOCKED, TOPIC_MOVED = 0, 1, 2
    STATUS_CHOICES = (
        (TOPIC_UNLOCKED, _('Topic unlocked')),
        (TOPIC_LOCKED, _('Topic locked')),
        (TOPIC_MOVED, _('Topic moved')),
    )
    status = models.PositiveIntegerField(
        choices=STATUS_CHOICES, db_index=True, verbose_name=_('Topic status'),
    )
    approved = models.BooleanField(default=True, db_index=True, verbose_name=_('Approved'))
    posts_count = models.PositiveIntegerField(
        editable=False, blank=True, default=0, verbose_name=_('Posts count'),
    )
    views_count = models.PositiveIntegerField(
        editable=False, blank=True, default=0, verbose_name=_('Views count'),
    )
    last_post_on = models.DateTimeField(
        blank=True,
        null=True,
        db_index=True,
        verbose_name=_('Last post added on')
    )
    first_post = models.ForeignKey(
        'forum_conversation.Post', editable=False, related_name='+', blank=True, null=True,
        on_delete=models.SET_NULL, verbose_name=_('First post'),
    )
    last_post = models.ForeignKey(
        'forum_conversation.Post', editable=False, related_name='+', blank=True, null=True,
        on_delete=models.SET_NULL, verbose_name=_('Last post'),
    )
    subscribers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='topic_subscriptions', blank=True,
        verbose_name=_('Subscribers'),
    )
    created = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name=_('Creation date')
    )
    updated = models.DateTimeField(
        auto_now=True,
        db_index=True,
        verbose_name=_('Update date')
    )

    objects = models.Manager()
    approved_objects = ApprovedManager()

    class Meta:
        abstract = True
        app_label = 'forum_conversation'
        indexes = [models.Index(fields=['type', 'last_post_on']), ]
        ordering = ['-type', '-last_post_on', ]
        get_latest_by = 'last_post_on'
        verbose_name = _('Topic')
        verbose_name_plural = _('Topics')

    def __str__(self):
        return self.first_post.subject if self.first_post is not None else self.subject

    @property
    def is_topic(self):
        return self.type == self.TOPIC_POST

    @property
    def is_sticky(self):
        return self.type == self.TOPIC_STICKY

    @property
    def is_announce(self):
        return self.type == self.TOPIC_ANNOUNCE

    @property
    def is_locked(self):
        return self.status == self.TOPIC_LOCKED

    def has_subscriber(self, user):
        if not hasattr(self, '_subscribers'):
            self._subscribers = list(self.subscribers.all())
        return user in self._subscribers

    def clean(self):
        super().clean()
        if self.forum.is_category or self.forum.is_link:
            raise ValidationError(_('A topic can not be associated with a category or a link forum'))

    def save(self, *args, **kwargs):
        old_instance = None
        if self.pk:
            old_instance = self.__class__._default_manager.get(pk=self.pk)
        self.slug = slugify(force_str(self.subject), allow_unicode=True) or 'topic'
        super().save(*args, **kwargs)
        if old_instance and old_instance.forum != self.forum:
            self.update_trackers()
            if old_instance.forum:
                old_forum = old_instance.forum
                old_forum.refresh_from_db()
                old_forum.update_trackers()

    def _simple_save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def delete(self, using=None):
        super().delete(using)
        self.forum.update_trackers()

    def update_trackers(self):
        self.posts_count = self.posts.filter(approved=True).count()
        first_post = self.posts.all().order_by('created').first()
        last_post = self.posts.filter(approved=True).order_by('-created').first()
        self.first_post = first_post
        self.last_post = last_post
        self.last_post_on = last_post.created if last_post else None
        self._simple_save()
        self.forum.update_trackers()


class AbstractPost(DatedModel):
    topic = models.ForeignKey(
        'forum_conversation.Topic', related_name='posts', on_delete=models.CASCADE,
        verbose_name=_('Topic'),
    )
    poster = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='posts',
        blank=True, null=True, on_delete=models.CASCADE, verbose_name=_('Poster'),
    )
    anonymous_key = models.CharField(
        max_length=100, blank=True, null=True, verbose_name=_('Anonymous user forum key'),
    )
    subject = models.CharField(verbose_name=_('Subject'), max_length=255)
    content = MarkupTextField(
        validators=[
            validators.MarkupMaxLengthValidator(machina_settings.POST_CONTENT_MAX_LENGTH),
        ],
        verbose_name=_('Content'),
    )
    username = models.CharField(max_length=155, blank=True, null=True, verbose_name=_('Username'))
    approved = models.BooleanField(default=True, db_index=True, verbose_name=_('Approved'))
    enable_signature = models.BooleanField(
        default=True, db_index=True, verbose_name=_('Attach a signature'),
    )
    update_reason = models.CharField(
        max_length=255, blank=True, null=True, verbose_name=_('Update reason'),
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, editable=False, blank=True, null=True, on_delete=models.SET_NULL,
        verbose_name=_('Lastly updated by'), related_name='updated_posts'
    )
    updates_count = models.PositiveIntegerField(
        editable=False, blank=True, default=0, verbose_name=_('Updates count'),
    )
    objects = models.Manager()
    approved_objects = ApprovedManager()

    class Meta:
        abstract = True
        app_label = 'forum_conversation'
        ordering = ['created', ]
        get_latest_by = 'created'
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')

    def __str__(self):
        return self.subject

    @property
    def is_topic_head(self):
        return self.topic.first_post.id == self.id if self.topic.first_post else False

    @property
    def is_topic_tail(self):
        return self.topic.last_post.id == self.id if self.topic.last_post else False

    @property
    def is_alone(self):
        return self.topic.posts.count() == 1

    @property
    def position(self):
        position = self.topic.posts.filter(Q(created__lt=self.created) | Q(id=self.id)).count()
        return position

    def clean(self):
        super().clean()
        if self.poster is None and self.anonymous_key is None:
            raise ValidationError(
                _('A user id or an anonymous key must be associated with a post.'),
            )
        if self.poster and self.anonymous_key:
            raise ValidationError(
                _('A user id or an anonymous key must be associated with a post, but not both.'),
            )
        if self.anonymous_key and not self.username:
            raise ValidationError(_('A username must be specified if the poster is anonymous'))

    def save(self, *args, **kwargs):
        new_post = self.pk is None
        super().save(*args, **kwargs)
        if (new_post and self.topic.first_post is None) or self.is_topic_head:
            if self.subject != self.topic.subject or self.approved != self.topic.approved:
                self.topic.subject = self.subject
                self.topic.approved = self.approved
        self.topic.update_trackers()

    def delete(self, using=None):
        if self.is_alone:
            self.topic.delete()
        else:
            super(AbstractPost, self).delete(using)
            self.topic.update_trackers()
