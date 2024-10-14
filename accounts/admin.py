"""
This module defines custom Django admin configurations for managing User and UserProfile models.

- The `UserProfileInline` class creates an inline display for the UserProfile model, allowing it to be shown within the User model's admin page. It restricts adding new profiles, making the 'cover_photo' field read-only.
- The `CustomUserAdmin` class extends the default UserAdmin from Django to include additional fields like 'profile_picture' and 'bio' from the custom User model, and displays UserProfile inline within the User admin page. It also customizes the list display, filters, and search fields in the User admin page.
- The `UserProfileAdmin` class defines how the UserProfile model is displayed on its own in the Django admin. It prevents the addition of new profiles and makes the 'cover_photo' field read-only.

Both models are then registered with the Django admin site using `admin.site.register`.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profile'
    fields = ('cover_photo',)  # Only include fields that are part of UserProfile
    readonly_fields = ('cover_photo',)  # Only include fields that are part of UserProfile

    def has_add_permission(self, request, obj=None):
        return False

class CustomUserAdmin(BaseUserAdmin):
    model = User
    inlines = (UserProfileInline,)
    list_display = ('email', 'username', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    readonly_fields = ('date_joined',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'profile_picture', 'bio')}),  # Include fields from User
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('date_joined', 'last_login')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'username')
    ordering = ('email',)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'cover_photo')  # Only include fields that are part of UserProfile
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('cover_photo',)

    def has_add_permission(self, request, obj=None):
        return False

admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
