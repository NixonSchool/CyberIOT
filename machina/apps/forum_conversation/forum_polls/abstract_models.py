from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from machina.apps.forum_conversation.forum_polls import validators
from machina.models.abstract_models import DatedModel


class AbstractTopicPoll(DatedModel):
    topic = models.OneToOneField(
        'forum_conversation.Topic', related_name='poll', on_delete=models.CASCADE,
        verbose_name=_('Topic'),
    )
    question = models.CharField(max_length=255, verbose_name=_('Poll question'))
    duration = models.PositiveIntegerField(
        verbose_name=_('Poll duration, in days'), blank=True, null=True,
    )
    max_options = models.PositiveSmallIntegerField(
        verbose_name=_('Maximum number of poll options per user'),
        validators=validators.poll_max_options, default=1,
    )
    user_changes = models.BooleanField(verbose_name=_('Allow vote changes'), default=False)
    hide_results = models.BooleanField(verbose_name=_('Hide results'), default=False)

    class Meta:
        abstract = True
        app_label = 'forum_polls'
        ordering = ['-updated', ]
        get_latest_by = 'updated'
        verbose_name = _('Topic poll')
        verbose_name_plural = _('Topic polls')

    def __str__(self):
        return '{}'.format(self.topic.subject)

    @cached_property
    def votes(self):
        votes = []
        for option in self.options.all():
            votes += option.votes.all()
        return votes


class AbstractTopicPollOption(models.Model):
    poll = models.ForeignKey(
        'forum_polls.TopicPoll', related_name='options', on_delete=models.CASCADE,
        verbose_name=_('Poll'),
    )
    text = models.CharField(max_length=255, verbose_name=_('Poll option text'))

    class Meta:
        abstract = True
        app_label = 'forum_polls'
        verbose_name = _('Topic poll option')
        verbose_name_plural = _('Topic poll options')

    def __str__(self):
        return '{} - {}'.format(self.poll, self.text)

    @cached_property
    def percentage(self):
        return (self.votes.count() / (len(self.poll.votes) or 1)) * 100


class AbstractTopicPollVote(models.Model):
    voter = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='poll_votes', blank=True, null=True,
        on_delete=models.CASCADE, verbose_name=_('Voter'),
    )
    anonymous_key = models.CharField(
        max_length=100, verbose_name=_('Anonymous user forum key'), blank=True, null=True,
    )
    poll_option = models.ForeignKey(
        'forum_polls.TopicPollOption', related_name='votes', on_delete=models.CASCADE,
        verbose_name=_('Poll option'),
    )
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name=_('Vote\'s date'))

    class Meta:
        abstract = True
        app_label = 'forum_polls'
        verbose_name = _('Topic poll vote')
        verbose_name_plural = _('Topic poll votes')

    def __str__(self):
        return '{} - {}'.format(self.poll_option, self.voter)

    def clean(self):
        super().clean()
        if self.voter is None and self.anonymous_key is None:
            raise ValidationError(_('A user id or an anonymous key must be used.'))
        if self.voter and self.anonymous_key:
            raise ValidationError(_('A user id or an anonymous key must be used, but not both.'))
