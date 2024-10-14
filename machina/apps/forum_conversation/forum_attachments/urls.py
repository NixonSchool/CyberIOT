from django.urls import path
from machina.core.loading import get_class
from machina.core.urls import URLPatternsFactory


class ForumAttachmentsURLPatternsFactory(URLPatternsFactory):
    attachment_view = get_class('forum_conversation.forum_attachments.views', 'AttachmentView')

    def get_urlpatterns(self):
        return [
            path('attachment/<int:pk>/', self.attachment_view.as_view(), name='attachment'),
        ]


urlpatterns_factory = ForumAttachmentsURLPatternsFactory()
