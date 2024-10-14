from django.urls import path
from . import views

app_name = 'chatzone2'

urlpatterns = [
    path('chat/', views.chat_home, name='chat_home'),  # Home view for chats and friends
    path('load_chat/<int:user_id>/', views.load_chat, name='load_chat'),  # Load chat for a specific user
    path('send_message/<int:user_id>/', views.send_message, name='send_message'),  # Send a message to a user
    path('get_new_messages/<int:user_id>/', views.get_new_messages, name='get_new_messages'),  # Fetch new messages
    path('direct_message/<int:user_id>/', views.direct_message, name='direct_message'),
    # Send direct message (supports files)

    path('send_friend_request/<int:user_id>/', views.send_friend_request, name='send_friend_request'),
    # Send friend request
    path('accept_friend_request/<int:request_id>/', views.accept_friend_request, name='accept_friend_request'),
    # Accept friend request

    path('friend_requests/', views.friend_requests, name='friend_requests'),  # View list of friend requests

    path('delete_chat/<int:user_id>/', views.delete_chat, name='delete_chat'),  # Delete chat with a user
    path('delete_message/<int:message_id>/', views.delete_message, name='delete_message'),  # Delete specific message

    path('search/', views.search_users, name='search_users'),  # Search for users

    path('cancel_friend_request/<int:request_id>/', views.cancel_friend_request, name='cancel_friend_request'),
    # Cancel sent friend request
    path('decline_friend_request/<int:request_id>/', views.decline_friend_request, name='decline_friend_request'),
    # Decline received friend request

    path('long_poll/<int:user_id>/', views.long_poll, name='long_poll'),  # Long polling for new messages
]
