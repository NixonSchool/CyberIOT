# This file defines the custom User and UserProfile models, along with the CustomUserManager for handling user creation,
# a signal to automatically create or update a UserProfile whenever a User instance is created or modified.
# no need for a separate signals.py file coz we already handle its functionality here.

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.conf import settings



class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field is required.'))
        if not username:
            raise ValueError(_('The Username field is required.'))

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, first_name, last_name, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('Email Address'), unique=True)
    username = models.CharField(_('Username'), max_length=150, unique=True)
    first_name = models.CharField(_('First Name'), max_length=30, blank=True)
    last_name = models.CharField(_('Last Name'), max_length=30, blank=True)
    profile_picture = models.ImageField(_('Profile Picture'), upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(_('Bio'), max_length=500, blank=True)
    is_active = models.BooleanField(_('Active'), default=True)
    is_staff = models.BooleanField(_('Staff status'), default=False)
    date_joined = models.DateTimeField(_('Date Joined'), default=timezone.now)
    password_reset_token = models.CharField(max_length=6, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')



class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_profile')
    profile_picture = models.ImageField(default='profile-pic-default.jpg', upload_to='profile_pics', blank=True, null=True)
    cover_photo = models.ImageField(_('Cover Photo'), upload_to='cover_photos/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=100, blank=True)
    twitter_url = models.CharField(max_length=250, default="#", blank=True, null=True)
    instagram_url = models.CharField(max_length=250, default="#", blank=True, null=True)
    facebook_url = models.CharField(max_length=250, default="#", blank=True, null=True)
    github_url = models.CharField(max_length=250, default="#", blank=True, null=True)
    email_confirmed = models.BooleanField(default=False)
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    class Meta:
        verbose_name = _('User Profile')
        verbose_name_plural = _('User Profiles')

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.user_profile.save()
