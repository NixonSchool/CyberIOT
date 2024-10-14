from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Count, Q
from marketitem.models import Item
from .forms import ConversationMessageForm
from .models import Conversation, ConversationMessage


@login_required
def inbox(request):
    conversations = Conversation.objects.filter(members__in=[request.user.id])

    # Add unread messages count for each conversation
    for conversation in conversations:
        conversation.unread_count = ConversationMessage.objects.filter(
            conversation=conversation
        ).exclude(
            read_by=request.user
        ).exclude(
            created_by=request.user
        ).count()

    return render(request, 'conversation/inbox.html', {
        'conversations': conversations,
    })


@login_required
def detail(request, pk):
    conversation = get_object_or_404(Conversation, pk=pk, members__in=[request.user.id])

    # Mark all messages in this conversation as read
    unread_messages = ConversationMessage.objects.filter(
        conversation=conversation
    ).exclude(
        read_by=request.user
    ).exclude(
        created_by=request.user
    )

    for message in unread_messages:
        message.read_by.add(request.user)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()
            conversation.save()  # Updates modified_at

            return redirect('marketchat:detail', pk=pk)
    else:
        form = ConversationMessageForm()

    return render(request, 'conversation/detail.html', {
        'conversation': conversation,
        'form': form,
    })


@login_required
def get_unread_message_count(request):
    unread_count = ConversationMessage.objects.filter(
        conversation__members=request.user
    ).exclude(
        read_by=request.user
    ).exclude(
        created_by=request.user
    ).count()

    return JsonResponse({
        'unread_count': unread_count
    })


@login_required
def new_conversation(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk)

    if item.created_by == request.user:
        return redirect('marketdash:index')

    conversations = Conversation.objects.filter(item=item, members__in=[request.user.id])

    if conversations.exists():
        return redirect('marketchat:detail', pk=conversations.first().id)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation = Conversation.objects.create(item=item)
            conversation.members.add(request.user)
            conversation.members.add(item.created_by)
            conversation.save()

            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            return redirect('marketitem:detail', pk=item_pk)
    else:
        form = ConversationMessageForm()

    return render(request, 'conversation/new.html', {
        'form': form,
    })