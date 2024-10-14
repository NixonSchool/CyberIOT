"""
The code defines views for a forum member application in Django, managing user
interactions with forum profiles and topics. It includes functionality to
display a user's posts, show their profile details, update their profile,
subscribe to or unsubscribe from topics, and list all topics they are
subscribed to. Each view utilizes Django's class-based views, integrating
permissions and context management to ensure that users can only interact with
content they have access to. The views also employ signals to handle post
counts and maintain user engagement within the forum.

"""
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, ListView, UpdateView
from django.views.generic.detail import BaseDetailView, SingleObjectTemplateResponseMixin

from machina.conf import settings as machina_settings
from machina.core.db.models import get_model
from machina.core.loading import get_class

Forum = get_model('forum', 'Forum')
ForumProfile = get_model('forum_member', 'ForumProfile')
Post = get_model('forum_conversation', 'Post')
Topic = get_model('forum_conversation', 'Topic')

ForumProfileForm = get_class('forum_member.forms', 'ForumProfileForm')

PermissionRequiredMixin = get_class('forum_permission.viewmixins', 'PermissionRequiredMixin')


class UserPostsView(ListView):
    context_object_name = 'posts'
    paginate_by = machina_settings.PROFILE_POSTS_NUMBER_PER_PAGE
    template_name = 'machina/forum_member/user_posts_list.html'
    user_pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['poster'] = self.poster
        return context

    def get_queryset(self):
        forums = self.request.forum_permission_handler.get_readable_forums(
            Forum.objects.all(), self.request.user,
        )
        return (
            Post.objects
            .select_related('topic', 'topic__forum', 'poster')
            .prefetch_related('poster__forum_profile')
            .filter(poster=self.poster, topic__forum__in=forums)
            .order_by('-created')
        )

    @cached_property
    def poster(self):
        user_model = get_user_model()
        return get_object_or_404(user_model, pk=self.kwargs[self.user_pk_url_kwarg])


class ForumProfileDetailView(DetailView):
    context_object_name = 'profile'
    template_name = 'machina/forum_member/forum_profile_detail.html'

    def get_queryset(self):
        user_model = get_user_model()
        return user_model.objects.all()

    def get_object(self, queryset=None):
        user = super().get_object(queryset)
        profile, dummy = ForumProfile.objects.get_or_create(user=user)
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topics_count'] = (
            Topic.objects.filter(approved=True, poster=self.object.user).count()
        )
        forums = self.request.forum_permission_handler.get_readable_forums(
            Forum.objects.all(), self.request.user,
        )
        recent_posts = (
            Post.approved_objects
            .select_related('topic', 'topic__forum')
            .filter(topic__forum__in=forums, poster=self.object.user)
            .order_by('-created')
        )
        context['recent_posts'] = recent_posts[:machina_settings.PROFILE_RECENT_POSTS_NUMBER]
        return context


class ForumProfileUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ForumProfileForm
    template_name = 'machina/forum_member/forum_profile_update.html'
    success_message = _('The profile has been edited successfully.')

    def get_object(self, queryset=None):
        profile, dummy = ForumProfile.objects.get_or_create(user=self.request.user)
        return profile

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response

    def get_success_url(self):
        return reverse('forum_member:profile_update')


class TopicSubscribeView(
    LoginRequiredMixin, PermissionRequiredMixin, SingleObjectTemplateResponseMixin, BaseDetailView,
):
    model = Topic
    success_message = _('You subscribed to this topic successfully.')
    template_name = 'machina/forum_member/topic_subscribe.html'

    def subscribe(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.subscribers.add(request.user)
        messages.success(self.request, self.success_message)
        return HttpResponseRedirect(self.get_success_url())

    def post(self, request, *args, **kwargs):
        return self.subscribe(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topic'] = self.object
        context['forum'] = self.object.forum
        return context

    def get_success_url(self):
        return reverse(
            'forum_conversation:topic',
            kwargs={
                'forum_slug': self.object.forum.slug,
                'forum_pk': self.object.forum.pk,
                'slug': self.object.slug,
                'pk': self.object.pk,
            },
        )

    def perform_permissions_check(self, user, obj, perms):
        return self.request.forum_permission_handler.can_subscribe_to_topic(obj, user)


class TopicUnsubscribeView(
    LoginRequiredMixin, PermissionRequiredMixin, SingleObjectTemplateResponseMixin, BaseDetailView,
):
    model = Topic
    success_message = _('You unsubscribed from this topic successfully.')
    template_name = 'machina/forum_member/topic_unsubscribe.html'

    def unsubscribe(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.subscribers.remove(request.user)
        messages.success(self.request, self.success_message)
        return HttpResponseRedirect(self.get_success_url())

    def post(self, request, *args, **kwargs):
        return self.unsubscribe(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topic'] = self.object
        context['forum'] = self.object.forum
        return context

    def get_success_url(self):
        return reverse(
            'forum_conversation:topic',
            kwargs={
                'forum_slug': self.object.forum.slug,
                'forum_pk': self.object.forum.pk,
                'slug': self.object.slug,
                'pk': self.object.pk,
            },
        )

    def perform_permissions_check(self, user, obj, perms):
        return self.request.forum_permission_handler.can_unsubscribe_from_topic(obj, user)


class TopicSubscriptionListView(LoginRequiredMixin, ListView):
    context_object_name = 'topics'
    model = Topic
    paginate_by = machina_settings.FORUM_TOPICS_NUMBER_PER_PAGE
    template_name = 'machina/forum_member/subscription_topic_list.html'

    def get_queryset(self):
        return (
            self.request.user.topic_subscriptions
            .select_related('forum', 'poster', 'last_post', 'last_post__poster')
            .all()
        )
