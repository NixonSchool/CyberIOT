# marketchat/templatetags/chat_tags.py
from django import template
from marketchat.models import ConversationMessage

register = template.Library()

@register.filter
def unread_message_count(user):
    return ConversationMessage.objects.filter(
        conversation__members=user
    ).exclude(
        read_by=user
    ).exclude(
        created_by=user
    ).count()