"""

This module defines an abstract model for managing attachments in a Django forum application.
The `AbstractAttachment` class links an attachment to a specific post and includes fields for the
attachment file and an optional comment.

It provides methods to get the upload path for the file
and to retrieve the filename. This abstract model can be inherited by other models to create
specific implementations for attachments without directly creating a database table.

"""
import os
from django.db import models
from django.utils.translation import gettext_lazy as _
from machina.conf import settings as machina_settings


def get_attachment_file_upload_to(instance, filename):
    return instance.get_file_upload_to(filename)


class AbstractAttachment(models.Model):
    post = models.ForeignKey(
        'forum_conversation.Post', related_name='attachments', on_delete=models.CASCADE,
        verbose_name=_('Post'),
    )
    file = models.FileField(upload_to=get_attachment_file_upload_to, verbose_name=_('File'))
    comment = models.CharField(max_length=255, verbose_name=_('Comment'), blank=True, null=True)

    class Meta:
        abstract = True
        app_label = 'forum_attachments'
        verbose_name = _('Attachment')
        verbose_name_plural = _('Attachments')

    def __str__(self):
        return '{}'.format(self.post.subject)

    @property
    def filename(self):
        return os.path.basename(self.file.name)

    def get_file_upload_to(self, filename):
        return os.path.join(machina_settings.ATTACHMENT_FILE_UPLOAD_TO, filename)
