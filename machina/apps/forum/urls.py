from django.urls import path
from machina.core.loading import get_class
from machina.core.urls import URLPatternsFactory


class ForumURLPatternsFactory(URLPatternsFactory):
    """Allows generating the URL patterns for the `forum` application."""

    app_namespace = 'forum'

    index_view = get_class('forum.views', 'IndexView')
    forum_view = get_class('forum.views', 'ForumView')

    def get_urlpatterns(self):
        """Returns the URL patterns managed by the factory."""
        return [
            path('', self.index_view.as_view(), name='index'),
            path(
                'forum/<str:slug>-<int:pk>/',
                self.forum_view.as_view(),
                name='forum',
            ),
        ]


urlpatterns = ForumURLPatternsFactory().get_urlpatterns()
