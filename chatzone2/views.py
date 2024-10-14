from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth import get_user_model
from .models import Message, FriendRequest, Friendship
from accounts.models import UserProfile
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.db.models import Q
from .models import Message
import time

User = get_user_model()


# Chat home view: display user's friends and messages
@login_required
def chat_home(request):
    friendships = Friendship.objects.filter(Q(user1=request.user) | Q(user2=request.user))
    friends = User.objects.filter(
        Q(friendships1__user2=request.user) | Q(friendships2__user1=request.user)
    ).distinct()

    friends_data = []
    for friend in friends:
        last_message = Message.objects.filter(
            Q(sender=request.user, recipient=friend) | Q(sender=friend, recipient=request.user)
        ).order_by('-timestamp').first()

        unread_count = Message.objects.filter(
            sender=friend, recipient=request.user, is_read=False
        ).count()

        friends_data.append({
            'user': friend,
            'profile': friend.user_profile,
            'last_message': last_message,
            'unread_count': unread_count
        })

    return render(request, 'chatzone/home.html', {'friends_data': friends_data})


# Load a specific chat between the user and another user
@login_required
def load_chat(request, user_id):
    chat_partner = get_object_or_404(User, id=user_id)
    messages = Message.objects.filter(
        Q(sender=request.user, recipient=chat_partner) | Q(sender=chat_partner, recipient=request.user)
    ).order_by('timestamp')

    # Mark messages as read
    unread_messages = messages.filter(recipient=request.user, is_read=False)
    unread_messages.update(is_read=True)

    messages_data = [{
        'content': msg.content,
        'timestamp': msg.timestamp.strftime('%H:%M'),
        'is_sender': msg.sender == request.user
    } for msg in messages]

    return JsonResponse({
        'chat_partner': chat_partner.username,
        'messages': messages_data
    })


@login_required
def send_message(request, user_id):
    if request.method == 'POST':
        recipient = get_object_or_404(User, id=user_id)
        content = request.POST.get('content', '')

        message = Message.objects.create(
            sender=request.user,
            recipient=recipient,
            content=content
        )

        return JsonResponse({
            'status': 'success',
            'message': {
                'content': message.content,
                'timestamp': message.timestamp.strftime('%H:%M'),
                'is_sender': True
            }
        })
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


@login_required
def get_new_messages(request, user_id):
    chat_partner = get_object_or_404(User, id=user_id)
    last_message_id = request.GET.get('last_message_id')

    new_messages = Message.objects.filter(
        Q(sender=request.user, recipient=chat_partner) | Q(sender=chat_partner, recipient=request.user),
        id__gt=last_message_id
    ).order_by('timestamp')

    # Mark new messages as read
    new_messages.filter(recipient=request.user, is_read=False).update(is_read=True)

    messages_data = [{
        'id': msg.id,
        'content': msg.content,
        'timestamp': msg.timestamp.strftime('%H:%M'),
        'is_sender': msg.sender == request.user
    } for msg in new_messages]

    return JsonResponse({
        'messages': messages_data
    })


# Send a direct message (supports text and file sharing)
@login_required
def direct_message(request, user_id):
    chat_partner = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        content = request.POST.get('content', '')
        file = request.FILES.get('file', None)

        message = Message.objects.create(
            sender=request.user,
            recipient=chat_partner,
            content=content,
            file=file
        )

        return JsonResponse({
            'status': 'success',
            'message': {
                'content': message.content,
                'timestamp': message.timestamp.strftime('%H:%M')
            }
        })
    # If the request method is GET, redirect to chat home
    return redirect('chatzone2:chat_home')


# Send a friend request
@login_required
def send_friend_request(request, user_id):
    if request.method == 'POST':
        recipient = get_object_or_404(User, id=user_id)

        # Check if a friendship already exists
        friendship_exists = Friendship.objects.filter(
            (Q(user1=request.user, user2=recipient) | Q(user1=recipient, user2=request.user))
        ).exists()

        if friendship_exists:
            return JsonResponse({'status': 'error', 'message': 'You are already friends with this user'})

        # Check if there's an existing request in either direction
        existing_request = FriendRequest.objects.filter(
            (Q(sender=request.user, recipient=recipient) | Q(sender=recipient, recipient=request.user))
        ).first()

        if existing_request:
            if existing_request.sender == request.user:
                return JsonResponse({'status': 'info', 'message': 'Friend request already sent'})
            else:
                # If the recipient has already sent a request, accept it
                existing_request.accept()
                return JsonResponse({'status': 'success', 'message': 'Friend request accepted'})

        # Create a new friend request
        FriendRequest.objects.create(sender=request.user, recipient=recipient)
        return JsonResponse({'status': 'success', 'message': 'Friend request sent successfully'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


@login_required
def cancel_friend_request(request, request_id):
    if request.method == 'POST':
        friend_request = get_object_or_404(FriendRequest, id=request_id, sender=request.user)
        recipient = friend_request.recipient
        friend_request.delete()
        messages.success(request, f'Friend request to {recipient.username} has been canceled.')
        return JsonResponse({'status': 'success', 'message': 'Friend request canceled'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


@login_required
def decline_friend_request(request, request_id):
    if request.method == 'POST':
        friend_request = get_object_or_404(FriendRequest, id=request_id, recipient=request.user)
        sender = friend_request.sender
        friend_request.delete()
        messages.success(request, f'Friend request from {sender.username} has been declined.')
        return JsonResponse({'status': 'success', 'message': 'Friend request declined'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


# Accept a friend request and create a friendship
@login_required
def accept_friend_request(request, request_id):
    if request.method == 'POST':
        friend_request = get_object_or_404(FriendRequest, id=request_id, recipient=request.user)
        sender = friend_request.sender

        # Create friendship after accepting the request
        Friendship.objects.create(user1=sender, user2=request.user)
        friend_request.delete()

        messages.success(request, f'You are now friends with {sender.username}.')
        return JsonResponse({'status': 'success', 'message': 'Friend request accepted'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


# List of friend requests for the logged-in user
@login_required
def friend_requests(request):
    received_requests = FriendRequest.objects.filter(recipient=request.user, is_accepted=False)
    request_profiles = {req.sender.id: req.sender.user_profile for req in received_requests}

    return render(request, 'chatzone/friend_requests.html', {
        'requests': received_requests,
        'request_profiles': request_profiles
    })


# Delete a chat with a specific user

@login_required
def delete_chat(request, user_id):
    chat_partner = get_object_or_404(User, id=user_id)
    Message.objects.filter(
        Q(sender=request.user, recipient=chat_partner) | Q(sender=chat_partner, recipient=request.user)
    ).delete()

    # Remove friendship
    Friendship.objects.filter(
        Q(user1=request.user, user2=chat_partner) | Q(user1=chat_partner, user2=request.user)
    ).delete()

    return JsonResponse({'status': 'success'})


# Delete a specific message
@login_required
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id, sender=request.user)
    message.delete_message()

    return JsonResponse({'status': 'success'})


# Search for users to send friend requests or start chats
# views.py

@login_required
def search_users(request):
    query = request.GET.get('query', '')
    users = User.objects.filter(username__icontains=query).exclude(id=request.user.id)
    users_profiles = {user.id: user.user_profile for user in users}

    # Get existing friend requests and friendships
    sent_requests = FriendRequest.objects.filter(sender=request.user)
    received_requests = FriendRequest.objects.filter(recipient=request.user)
    friendships = Friendship.objects.filter(Q(user1=request.user) | Q(user2=request.user))

    # Create dictionaries for easier lookup in the template
    sent_requests_dict = {req.recipient_id: req.id for req in sent_requests}
    received_requests_dict = {req.sender_id: req.id for req in received_requests}
    friends_set = set(
        friendships.values_list('user1_id', flat=True).union(friendships.values_list('user2_id', flat=True)))
    friends_set.discard(request.user.id)

    context = {
        'users': users,
        'users_profiles': users_profiles,
        'sent_requests': sent_requests_dict,
        'received_requests': received_requests_dict,
        'friends': friends_set,
    }

    return render(request, 'chatzone/search_results.html', context)


def long_poll(request, user_id):
    last_message_id = request.GET.get('last_message_id', 0)
    timeout = 30  # Maximum time to keep the request open, in seconds
    start_time = time.time()

    while time.time() - start_time < timeout:
        messages = Message.objects.filter(
            Q(sender_id=request.user.id, recipient_id=user_id) |
            Q(sender_id=user_id, recipient_id=request.user.id),
            id__gt=last_message_id
        ).order_by('timestamp')

        if messages.exists():
            return JsonResponse({
                'messages': [{
                    'id': msg.id,
                    'content': msg.content,
                    'timestamp': msg.timestamp.strftime('%H:%M'),
                    'sender_id': msg.sender_id
                } for msg in messages]
            })

        time.sleep(1)  # Wait for 1 second before checking again

    # If no new messages after timeout, return an empty response
    return JsonResponse({'messages': []})