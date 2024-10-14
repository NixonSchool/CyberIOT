from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

# Import URL patterns factories
from machina.apps.forum.urls import urlpatterns as forum_urlpatterns
from machina.apps.forum_conversation.urls import urlpatterns_factory as forum_conversation_urlpatterns_factory
from machina.apps.forum_conversation.forum_polls.urls import urlpatterns_factory as forum_polls_urlpatterns_factory
from machina.apps.forum_conversation.forum_attachments.urls import \
    urlpatterns_factory as forum_attachments_urlpatterns_factory

from machina.apps.forum_member.urls import ForumMemberURLPatternsFactory
from machina.apps.forum_feeds.urls import ForumFeedsURLPatternsFactory
from machina.apps.forum_moderation.urls import ForumModerationURLPatternsFactory
from machina.apps.forum_tracking.urls import ForumTrackingURLPatternsFactory

# Instantiate the URL patterns factories
forum_member_urlpatterns_factory = ForumMemberURLPatternsFactory()
forum_feeds_urlpatterns_factory = ForumFeedsURLPatternsFactory()
forum_moderation_urlpatterns_factory = ForumModerationURLPatternsFactory()
forum_tracking_urlpatterns_factory = ForumTrackingURLPatternsFactory()

urlpatterns = [
                  # Admin
                  path('admin/', admin.site.urls),

                  # User Accounts and Profiles
                  path('accounts/', include('accounts.urls')),
                  path('profiles/', include('profiles.urls', namespace='profiles')),

                  # Mainpage
                  path('mainpage/', include('mainpage.urls')),
                  path('tinymce/', include('tinymce.urls')),

                  # Terms and Conditions
                  path('terms/', include('terms.urls')),

                  # Redirect root URL to log in
                  path('', RedirectView.as_view(url='/accounts/login/', permanent=False), name='home_redirect'),

                  # Market-related URLs
                  path('marketcore/', include('marketcore.urls')),
                  path('marketchat/', include('marketchat.urls')),
                  path('marketdash/', include('marketdash.urls')),
                  path('marketitem/', include('marketitem.urls')),


                  # Video Gallery and Channels
                  path('channels/', include('channel.urls', namespace='channel')),
                  path('video/', include('video.urls', namespace='video')),
                  path('account/', include('channelaccount.urls', namespace='account')),

                  # Vulnerabilities
                  path('exploits/', include('exploits.urls')),

                  # CKEditor
                  path('ckeditor/', include('ckeditor_uploader.urls')),

                  # Forum URLs
                  path('forum/', include((forum_urlpatterns, 'forum'), namespace='forum')),

                  # Forum Search URLs
                  path('forum/search/', include('machina.apps.forum_search.urls', namespace='forum_search')),

                  # Forum Member URLs
                  path('forum/member/', include((forum_member_urlpatterns_factory.get_urlpatterns(), 'forum_member'),
                                                namespace='forum_member')),

                  # Forum Feeds URLs
                  path('forum/feeds/', include((forum_feeds_urlpatterns_factory.get_urlpatterns(), 'forum_feeds'),
                                               namespace='forum_feeds')),

                  # Forum Moderation URLs
                  path('forum/moderation/',
                       include((forum_moderation_urlpatterns_factory.get_urlpatterns(), 'forum_moderation'),
                               namespace='forum_moderation')),

                  # Forum Tracking URLs
                  path('forum/tracking/',
                       include((forum_tracking_urlpatterns_factory.get_urlpatterns(), 'forum_tracking'),
                               namespace='forum_tracking')),

                  # New Forum Conversation URLs
                  path('forum/conversation/',
                       include((forum_conversation_urlpatterns_factory.get_urlpatterns(), 'forum_conversation'),
                               namespace='forum_conversation')),

                  # New Forum Polls URLs
                  path('forum/polls/', include((forum_polls_urlpatterns_factory.get_urlpatterns(), 'forum_polls'),
                                               namespace='forum_polls')),

                  # New Forum Attachments URLs
                  path('forum/attachments/',
                       include((forum_attachments_urlpatterns_factory.get_urlpatterns(), 'forum_attachments'),
                               namespace='forum_attachments')),

                  path('settings/', include('settings.urls')),

                  # Core Vulnerability tracking URLs
                  path('bug/', include('bug.urls', namespace='bug')),
                  path('summernote/', include('django_summernote.urls')),
                  path('chatzone/', include(('chatzone2.urls', 'chatzone2'), namespace='chatzone2')),


              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
