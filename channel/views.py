from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from .models import Channel
from .forms import ChannelForm
from video.models import Video
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# For searching
from django.db.models import Q


@login_required
def subscribeView(request, id):
    # Fetch the channel using the id from the URL
    channel = get_object_or_404(Channel, id=id)

    # Prevent subscribing to one's own channel
    if channel.user == request.user:
        messages.warning(request, 'You cannot subscribe to your own channel!')
        return redirect('channel:channelDetail', id=id)

    # Check if the user is already subscribed and toggle the subscription
    if channel.subscribers.filter(id=request.user.id).exists():
        channel.subscribers.remove(request.user)
        messages.success(request, 'You have unsubscribed from the channel.')
    else:
        channel.subscribers.add(request.user)
        messages.success(request, 'You have subscribed to the channel.')

    # Get the previous URL or fallback to the channel detail page
    referer_url = request.META.get('HTTP_REFERER', None)
    if referer_url:
        return HttpResponseRedirect(referer_url)
    else:
        return redirect('channel:channelDetail', id=id)


# @login_required
# def subscribeView(request, id):
#     if Channel.objects.filter(user_id=request.user.id).exists():
#         channel = get_object_or_404(
#             Channel, id=request.POST.get('video_subscribe_id'))
#
#         if channel.user == request.user:
#             messages.warning(request, 'You cannot subscribe to your own channel!')
#             return redirect('channel:channelDetail', id=id)
#
#         subscribe = False
#         if channel.subscribers.filter(id=request.user.id).exists():
#             channel.subscribers.remove(request.user)
#             subscribe = False
#         else:
#             channel.subscribers.add(request.user)
#             subscribe = True
#
#         url = request.META.get('HTTP_REFERER')
#     else:
#         messages.warning(
#             request, 'You must create a channel to subscribe channels!')
#         return redirect('channel:createChannel')
#
#     return HttpResponseRedirect(url)
#

def channelList(request):
    channels = Channel.objects.all()[:10]
    context = {
        'channels': channels,
    }
    return render(request, 'channel/channel_list.html', context)


def channelDetail(request, id):
    channel = Channel.objects.get(id=id)
    videos = Video.objects.filter(status="True", channel_id=id)

    subscribe = False
    if channel.subscribers.filter(id=request.user.id).exists():
        subscribe = True

    context = {
        'channel': channel,
        'videos': videos,
        'last_video': videos.last(),
        'subscribe': subscribe,
        'subscribe_total': channel.total_subscribers(),
    }

    return render(request, 'channel/channel_detail.html', context)


@login_required
def createChannel(request):
    if not Channel.objects.filter(user_id=request.user.id).exists():
        channelForm = ChannelForm(request.POST or None, request.FILES or None)
        if request.method == "POST":
            if channelForm.is_valid():
                channelForm.instance.user_id = request.user.id
                channel = channelForm.save()
                messages.success(
                    request, 'Your channel has been successfully created.')
                return HttpResponseRedirect(channel.get_absolute_url())
    else:
        userChannel = Channel.objects.get(user_id=request.user.id)
        messages.warning(request, 'You already own a channel!')
        return HttpResponseRedirect(userChannel.get_absolute_url())

    return render(request, 'channel/post/create_channel.html', {'channelForm': channelForm})


@login_required
def updateChannel(request, id):
    if Channel.objects.filter(user_id=request.user.id).exists():
        channel = Channel.objects.get(id=id, user_id=request.user.id)
        channelForm = ChannelForm(
            request.POST or None, request.FILES or None, instance=channel)
        if request.method == "POST":
            if channelForm.is_valid():
                channelForm.instance.user_id = request.user.id
                channelForm.save()
                messages.success(
                    request, 'Your channel has been successfully created.')
                return HttpResponseRedirect(channel.get_absolute_url())
    else:
        messages.warning(request, 'Please create your channel!')
        return redirect('video:createChannel')

    return render(request, 'channel/post/update_channel.html', {'channelForm': channelForm})


@login_required
def deleteChannel(request, id):
    if Channel.objects.filter(user_id=request.user.id).exists():
        channel = Channel.objects.get(id=id, user_id=request.user.id)
        try:
            channel.delete()
            messages.success(
                request, "Your channel has been successfully deleted.")
        except:
            messages.error(request, "Your channel could not be deleted!")
    else:
        messages.warning(request, 'Please create your channel!')
        return redirect('video:createChannel')

    return redirect('video:index')


@login_required
def subscriptionsList(request):
    channels = Channel.objects.filter(subscribers=request.user)
    videos = Video.objects.filter(channel__in=channels)
    context = {
        'channels': channels,
        'videos': videos
    }
    return render(request, 'channel/subscriptions_list.html', context)


# Adding a search view for the search button is not working
def search(request):
    query = request.GET.get('q', '')
    channel_results = []
    video_results = []

    if query:
        # Search in Channel's channel_name and description
        channel_results = Channel.objects.filter(
            Q(channel_name__icontains=query) | Q(description__icontains=query)
        )

        # Search in Video title and content
        video_results = Video.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )

    context = {
        'query': query,
        'channel_results': channel_results,
        'video_results': video_results,
    }
    return render(request, 'base/search_results.html', context)