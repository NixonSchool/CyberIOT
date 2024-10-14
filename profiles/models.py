from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    title = models.CharField(max_length=100, blank=True, default='')
    phone_number = models.CharField(max_length=20, blank=True, default='')
    skills = models.TextField(blank=True, default='', help_text="Comma-separated list of skills")
    education = models.TextField(blank=True, default='')
    experience = models.TextField(blank=True, default='')
    cover_photo = models.ImageField(upload_to='cover_photos/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}".strip()

    @property
    def bio(self):
        return self.user.user_profile.bio

    @property
    def profile_picture(self):
        return self.user.user_profile.profile_picture

    @property
    def job_title(self):
        return self.user.user_profile.job_title

    @property
    def address(self):
        return self.user.user_profile.address

    @property
    def city(self):
        return self.user.user_profile.city

    @property
    def country(self):
        return self.user.user_profile.country

    @property
    def zip_code(self):
        return self.user.user_profile.zip_code

    @property
    def twitter_url(self):
        return self.user.user_profile.twitter_url

    @property
    def instagram_url(self):
        return self.user.user_profile.instagram_url

    @property
    def facebook_url(self):
        return self.user.user_profile.facebook_url

    @property
    def github_url(self):
        return self.user.user_profile.github_url

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()