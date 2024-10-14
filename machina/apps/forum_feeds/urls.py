from django.urls import path
from machina.core.loading import get_class
from machina.core.urls import URLPatternsFactory


class ForumFeedsURLPatternsFactory(URLPatternsFactory):
    app_namespace = 'forum_feeds'
    latest_topics_feed = get_class('forum_feeds.feeds', 'LastTopicsFeed')

    def get_urlpatterns(self):
        return [
            path('topics/', self.latest_topics_feed(), name='latest_topics'),
            path(
                'forum/<str:forum_slug>-<int:forum_pk>/topics/',
                self.latest_topics_feed(),
                name='forum_latest_topics',
            ),
            path(
                'forum/<str:forum_slug>-<int:forum_pk>/topics/all/',
                self.latest_topics_feed(),
                {'descendants': True},
                name='forum_latest_topics_with_descendants',
            ),
        ]


urlpatterns_factory = ForumFeedsURLPatternsFactory()
