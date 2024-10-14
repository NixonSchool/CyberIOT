from django import forms
from .models import Profile
from django.contrib.auth import get_user_model

User = get_user_model()

class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), required=False)
    profile_picture = forms.ImageField(required=False)
    cover_photo = forms.ImageField(required=False)
    job_title = forms.CharField(max_length=100, required=False)
    address = forms.CharField(max_length=100, required=False)
    city = forms.CharField(max_length=100, required=False)
    country = forms.CharField(max_length=100, required=False)
    zip_code = forms.CharField(max_length=100, required=False)
    twitter_url = forms.URLField(required=False)
    instagram_url = forms.URLField(required=False)
    facebook_url = forms.URLField(required=False)
    github_url = forms.URLField(required=False)

    class Meta:
        model = Profile
        fields = ['title', 'phone_number', 'skills', 'education', 'experience', 'cover_photo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
            self.fields['bio'].initial = self.instance.bio
            self.fields['profile_picture'].initial = self.instance.profile_picture
            self.fields['cover_photo'].initial = self.instance.cover_photo
            self.fields['job_title'].initial = self.instance.job_title
            self.fields['address'].initial = self.instance.address
            self.fields['city'].initial = self.instance.city
            self.fields['country'].initial = self.instance.country
            self.fields['zip_code'].initial = self.instance.zip_code
            self.fields['twitter_url'].initial = self.instance.twitter_url
            self.fields['instagram_url'].initial = self.instance.instagram_url
            self.fields['facebook_url'].initial = self.instance.facebook_url
            self.fields['github_url'].initial = self.instance.github_url

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user_profile = user.user_profile
        user_profile.bio = self.cleaned_data['bio']
        user_profile.profile_picture = self.cleaned_data['profile_picture']
        user_profile.cover_photo = self.cleaned_data['cover_photo']
        user_profile.job_title = self.cleaned_data['job_title']
        user_profile.address = self.cleaned_data['address']
        user_profile.city = self.cleaned_data['city']
        user_profile.country = self.cleaned_data['country']
        user_profile.zip_code = self.cleaned_data['zip_code']
        user_profile.twitter_url = self.cleaned_data['twitter_url']
        user_profile.instagram_url = self.cleaned_data['instagram_url']
        user_profile.facebook_url = self.cleaned_data['facebook_url']
        user_profile.github_url = self.cleaned_data['github_url']

        if commit:
            user.save()
            user_profile.save()
            profile.save()
        return profile