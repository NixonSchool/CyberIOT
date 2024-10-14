"""
The code defines signal receivers in a Django application to manage the post count
of forum members based on their interactions with posts. It listens for the
`pre_save` and `post_delete` signals from the `Post` model. When a post is saved,
it increases the corresponding user's post count if the post is approved; when a
post is unapproved or deleted, it decreases the count if the post was previously
approved. The code ensures that these updates are only applied to valid users and
approved posts, maintaining accurate post counts in the `ForumProfile` model
associated with each user.

"""
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from machina.core.db.models import get_model

User = get_user_model()
Post = get_model('forum_conversation', 'Post')
ForumProfile = get_model('forum_member', 'ForumProfile')


@receiver(pre_save, sender=Post)
def increase_posts_count(sender, instance, **kwargs):
    if kwargs.get('raw'):
        return
    if instance.poster is None:
        return
    profile, dummy = ForumProfile.objects.get_or_create(user=instance.poster)
    increase_posts_count = False
    if instance.pk:
        try:
            old_instance = instance.__class__._default_manager.get(pk=instance.pk)
        except ObjectDoesNotExist:
            increase_posts_count = True
            old_instance = None
        if old_instance and old_instance.approved is False and instance.approved is True:
            increase_posts_count = True
    elif instance.approved:
        increase_posts_count = True
    if increase_posts_count:
        profile.posts_count = F('posts_count') + 1
        profile.save()


@receiver(pre_save, sender=Post)
def decrease_posts_count_after_post_unaproval(sender, instance, **kwargs):
    if kwargs.get('raw'):
        return
    if not instance.pk or not instance.poster:
        return
    profile, dummy = ForumProfile.objects.get_or_create(user=instance.poster)
    try:
        old_instance = instance.__class__._default_manager.get(pk=instance.pk)
    except ObjectDoesNotExist:
        return
    if old_instance and old_instance.approved is True and instance.approved is False:
        profile.posts_count = F('posts_count') - 1
        profile.save()


@receiver(post_delete, sender=Post)
def decrease_posts_count_after_post_deletion(sender, instance, **kwargs):
    if not instance.approved:
        return
    try:
        assert instance.poster_id is not None
        poster = User.objects.get(pk=instance.poster_id)
    except AssertionError:
        return
    except ObjectDoesNotExist:
        return
    profile, dummy = ForumProfile.objects.get_or_create(user=poster)
    if profile.posts_count:
        profile.posts_count = F('posts_count') - 1
        profile.save()
