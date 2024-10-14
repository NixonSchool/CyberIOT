from django.contrib import admin
from .models import Message, FriendRequest, Friendship


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'content', 'file', 'timestamp', 'is_read')
    list_filter = ('is_read', 'timestamp')
    search_fields = ('sender__username', 'recipient__username', 'content')
    ordering = ('-timestamp',)


@admin.register(FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('sender__username', 'recipient__username')
    ordering = ('-timestamp',)


@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    list_display = ('user1', 'user2', 'timestamp')
    search_fields = ('user1__username', 'user2__username')
    ordering = ('-timestamp',)
