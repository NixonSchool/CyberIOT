from django.shortcuts import render
from django.urls import reverse
from django.templatetags.static import static


def main_page(request):
    modules = [
        {
            'title': 'Forums',
            'description': ' Simple discussion forum.',
            'url': reverse('forum:index'),
            'image': static('mainpage/images/forum.png')
        },
        {
            'title': 'IoT Marketplace',
            'description': 'A centralized hub for IoT-related resources.',
            'url': reverse('marketcore:index'),
            'image': static('mainpage/images/marketplace.png')
        },
        {
            'title': 'LearningHub',
            'description': 'Access a dedicated educational section with IoT security resources.',
            'url': reverse('channel:channelList'),
            'image': static('mainpage/images/learninghub.png')
        },
        {
            'title': 'VulnerabilitiesHub',
            'description': 'Submit detailed information about discovered vulnerabilities.',
            'url': reverse('exploits:vulnerability_list'),
            'image': static('mainpage/images/vulnerabilities.png')
        },
        {
            'title': 'Vulnerability tracking',
            'description': 'CyberIOT site updates, fixed vulnerabilities, personal articles allowed.',
            'url': reverse('bug:home'),
            'image': static('mainpage/images/bloggy.png')
        },
        {
            'title': 'Messaging',
            'description': 'Private communication between users.',
            'url': reverse('chatzone2:chat_home'),
            'image': static('mainpage/images/messaging.png')
        },

    ]

    context = {
        'modules': modules,
        'user': request.user,
    }
    return render(request, 'mainpage/mainpage.html', context)
