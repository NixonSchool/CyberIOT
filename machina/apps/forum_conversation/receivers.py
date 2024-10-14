"""

This code defines a signal receiver that increments
the view counter for a topic each time it is viewed.

`F` is a Django expression used to reference model field values directly
in database queries, allowing for operations like incrementing a field's value;

`receiver` is a decorator that connects a function to a signal,
 enabling the function to execute when the specified signal is sent.

"""

from django.db.models import F
from django.dispatch import receiver
from machina.apps.forum_conversation.signals import topic_viewed


@receiver(topic_viewed)
def update_topic_counter(sender, topic, user, request, response, **kwargs):
    topic.__class__._default_manager.filter(id=topic.id).update(views_count=F('views_count') + 1)
