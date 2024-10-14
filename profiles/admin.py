from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'phone_number', 'full_name', 'bio', 'job_title')
    search_fields = ('user__username', 'user__email', 'title', 'phone_number', 'user__profile__job_title')
    list_filter = ('user__is_active', 'user__date_joined')
    readonly_fields = ('full_name', 'bio', 'profile_picture', 'job_title', 'address', 'city', 'country', 'zip_code', 'twitter_url', 'instagram_url', 'facebook_url', 'github_url')

    # Custom method to display bio
    def bio(self, obj):
        return obj.bio

    # Custom method to display profile picture
    def profile_picture(self, obj):
        return obj.profile_picture.url if obj.profile_picture else 'No Image'

    # Custom method to display job title
    def job_title(self, obj):
        return obj.job_title

    # Custom method to display address
    def address(self, obj):
        return obj.address

    # Custom method to display city
    def city(self, obj):
        return obj.city

    # Custom method to display country
    def country(self, obj):
        return obj.country

    # Custom method to display zip code
    def zip_code(self, obj):
        return obj.zip_code

    # Custom method to display Twitter URL
    def twitter_url(self, obj):
        return obj.twitter_url

    # Custom method to display Instagram URL
    def instagram_url(self, obj):
        return obj.instagram_url

    # Custom method to display Facebook URL
    def facebook_url(self, obj):
        return obj.facebook_url

    # Custom method to display GitHub URL
    def github_url(self, obj):
        return obj.github_url

    # Optional: Customize save behavior
    def save_model(self, request, obj, form, change):
        # You can add additional logic before saving if needed
        super().save_model(request, obj, form, change)

admin.site.register(Profile, ProfileAdmin)
