"""
The `TopicPollVoteView` is a Django view that allows users to vote in a forum poll.
It inherits from `UpdateView` and requires user permissions to access.
When a valid voting form is submitted, it creates or updates the user's votes
based on the selected options, deleting any previous votes if re-voting is allowed.
If the form submission is invalid, it displays error messages and redirects
the user back to the relevant topic page. Upon successfully casting a vote,
it shows a success message and redirects to the topic's page,
maintaining context about the forum and topic being voted on.

"""

from django.contrib import messages
from django.forms.forms import NON_FIELD_ERRORS
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import UpdateView
from django.views.generic.edit import ModelFormMixin

from machina.core.db.models import get_model
from machina.core.loading import get_class

TopicPoll = get_model('forum_polls', 'TopicPoll')
TopicPollVote = get_model('forum_polls', 'TopicPollVote')

TopicPollVoteForm = get_class('forum_polls.forms', 'TopicPollVoteForm')

PermissionRequiredMixin = get_class('forum_permission.viewmixins', 'PermissionRequiredMixin')


class TopicPollVoteView(PermissionRequiredMixin, UpdateView):
    form_class = TopicPollVoteForm
    http_method_names = ['post', ]
    model = TopicPoll

    def get_form_kwargs(self):
        kwargs = super(ModelFormMixin, self).get_form_kwargs()
        kwargs['poll'] = self.object
        return kwargs

    def form_valid(self, form):
        user_kwargs = (
            {'voter': self.request.user}
            if self.request.user.is_authenticated
            else {'anonymous_key': self.request.user.forum_key}
        )

        if self.object.user_changes:
            TopicPollVote.objects.filter(poll_option__poll=self.object, **user_kwargs).delete()

        options = form.cleaned_data['options']
        for option in options:
            TopicPollVote.objects.create(poll_option=option, **user_kwargs)

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, form.errors[NON_FIELD_ERRORS])
        return redirect(
            reverse(
                'forum_conversation:topic',
                kwargs={
                    'forum_slug': self.object.topic.forum.slug,
                    'forum_pk': self.object.topic.forum.pk,
                    'slug': self.object.topic.slug,
                    'pk': self.object.topic.pk
                },
            ),
        )

    def get_success_url(self):
        messages.success(self.request, _('Your vote has been cast.'))
        return reverse(
            'forum_conversation:topic',
            kwargs={
                'forum_slug': self.object.topic.forum.slug,
                'forum_pk': self.object.topic.forum.pk,
                'slug': self.object.topic.slug,
                'pk': self.object.topic.pk,
            },
        )

    def get_controlled_object(self):
        return self.get_object()

    def perform_permissions_check(self, user, obj, perms):
        return self.request.forum_permission_handler.can_vote_in_poll(obj, user)
