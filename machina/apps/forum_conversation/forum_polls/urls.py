from django.urls import path
from machina.core.loading import get_class
from machina.core.urls import URLPatternsFactory


class ForumPollsURLPatternsFactory(URLPatternsFactory):
    poll_vote_view = get_class('forum_conversation.forum_polls.views', 'TopicPollVoteView')

    def get_urlpatterns(self):
        return [
            path('poll/<int:pk>/vote/', self.poll_vote_view.as_view(), name='topic_poll_vote'),
        ]


urlpatterns_factory = ForumPollsURLPatternsFactory()
