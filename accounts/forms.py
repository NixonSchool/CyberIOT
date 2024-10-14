# forms.py
# This file defines custom forms for user creation, authentication, and password reset functionality,
# extending the default Django forms to include additional fields and custom validation logic.

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import UserProfile
from django.core.exceptions import ValidationError

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    profile_picture = forms.ImageField(required=False)
    bio = forms.CharField(widget=forms.Textarea, max_length=500, required=False)

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]

        if commit:
            user.save()
            user_profile = UserProfile.objects.get(user=user)
            user_profile.profile_picture = self.cleaned_data.get("profile_picture")
            user_profile.bio = self.cleaned_data.get("bio")
            user_profile.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Username or Email', widget=forms.TextInput(attrs={'autofocus': True}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Enter your username or email'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Enter your password'})

    error_messages = {
        'invalid_login': "Please enter a correct username or email and password. Note that both fields may be case-sensitive.",
        'inactive': "This account is inactive.",
    }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if '@' in username:
            try:
                user = User.objects.get(email=username)
                return user.username
            except User.DoesNotExist:
                raise ValidationError("No user found with this email address.")
        return username

class PasswordResetRequestForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Enter username (optional)'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'})
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')

        if not email:
            raise forms.ValidationError("Email is required.")

        return cleaned_data