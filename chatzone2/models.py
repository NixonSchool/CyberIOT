from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

# Use AUTH_USER_MODEL for user references
User = settings.AUTH_USER_MODEL


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField(_('Content'), blank=True)
    file = models.FileField(_('File'), upload_to='chatzone_files/', null=True, blank=True)
    timestamp = models.DateTimeField(_('Timestamp'), auto_now_add=True)
    is_read = models.BooleanField(_('Is Read'), default=False)

    def __str__(self):
        return f"Message from {self.sender} to {self.recipient}: {self.content[:50]}"

    def delete_message(self):
        self.delete()

    class Meta:
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')
        ordering = ['-timestamp']


class FriendRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests')
    timestamp = models.DateTimeField(_('Timestamp'), auto_now_add=True)

    def __str__(self):
        return f"Friend request from {self.sender} to {self.recipient}"

    def accept(self):
        Friendship.objects.create(user1=self.sender, user2=self.recipient)
        self.delete()

    class Meta:
        verbose_name = _('Friend Request')
        verbose_name_plural = _('Friend Requests')
        unique_together = ['sender', 'recipient']


class Friendship(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendships1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendships2')
    timestamp = models.DateTimeField(_('Timestamp'), auto_now_add=True)

    def __str__(self):
        return f"Friendship between {self.user1} and {self.user2}"

    class Meta:
        verbose_name = _('Friendship')
        verbose_name_plural = _('Friendships')
        unique_together = ['user1', 'user2']
