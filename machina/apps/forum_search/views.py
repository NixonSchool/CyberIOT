from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator
from machina.core.db.models import get_model
from machina.core.loading import get_class
from .forms import SearchForm

Post = get_model('forum_conversation', 'Post')
Topic = get_model('forum_conversation', 'Topic')
Forum = get_model('forum', 'Forum')
PermissionHandler = get_class('forum_permission.handler', 'PermissionHandler')


def search_view(request):
    form = SearchForm(request.GET)
    results = []

    if form.is_valid() and form.cleaned_data.get('q'):
        query = form.cleaned_data['q']

        # Get forums the user is allowed to read
        permission_handler = PermissionHandler()
        allowed_forums = permission_handler.get_readable_forums(Forum.objects.all(), request.user)

        # Modified query to only return posts that directly match the search term
        queryset = Post.objects.filter(
            Q(content__icontains=query) | Q(subject__icontains=query),
            topic__forum__in=allowed_forums
        ).distinct()

        results = queryset.select_related('topic', 'poster').order_by('-created')

        paginator = Paginator(results, 20)  # Show 20 results per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    context = {
        'form': form,
        'results': page_obj,  # Pass the page object instead of the raw results
    }

    return render(request, 'machina/forum_search/search.html', context)
