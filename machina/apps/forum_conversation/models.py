"""

This code defines the `Topic` and `Post` models by creating concrete
 implementations from their respective abstract base classes
 in the `forum_conversation` application.

"""

from machina.apps.forum_conversation.abstract_models import AbstractPost, AbstractTopic
from machina.core.db.models import model_factory

Topic = model_factory(AbstractTopic)
Post = model_factory(AbstractPost)
