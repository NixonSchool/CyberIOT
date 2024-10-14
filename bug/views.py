from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic, View
from django.views.generic.edit import FormMixin, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.contrib import messages
from .forms import CommentForm, PostForm
from .models import Post
from django.utils import timezone

def latest_post(request):
    latest = Post.objects.latest('created_on')
    return JsonResponse({'id': latest.id, 'title': latest.title})

class PostList(generic.ListView):
    template_name = "bughub_templates/index.html"
    paginate_by = 5
    context_object_name = 'post_list'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            # Show public posts and user's private posts
            return Post.objects.filter(
                Q(privacy='public') | Q(author=self.request.user)
            ).order_by("-created_on")
        # Show only public posts to anonymous users
        return Post.objects.filter(privacy='public').order_by("-created_on")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['recent_posts'] = Post.objects.filter(
                Q(privacy='public') | Q(author=self.request.user)
            ).order_by("-created_on")[:5]
        else:
            context['recent_posts'] = Post.objects.filter(
                privacy='public'
            ).order_by("-created_on")[:5]
        return context


class PostDetail(FormMixin, generic.DetailView):
    model = Post
    template_name = "bughub_templates/post_detail.html"
    form_class = CommentForm
    context_object_name = 'post'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not obj.is_visible_to(self.request.user):
            raise Http404("Post not found")
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.filter(active=True).order_by("-created_on")
        context['comment_form'] = self.get_form()
        context['recent_posts'] = Post.objects.order_by("-created_on")[:5]
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        new_comment = form.save(commit=False)
        new_comment.post = self.object
        new_comment.active = True
        new_comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class AddPost(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "bughub_templates/add_post.html"
    success_url = reverse_lazy('bug:home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, 'Your post has been created successfully!')
        return response


class EditPost(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "bughub_templates/edit_post.html"

    def get_success_url(self):
        return reverse_lazy('bug:post_detail', kwargs={'slug': self.object.slug})

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Your post has been updated successfully!')
        return response

class DeletePost(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('bug:home')
    template_name = 'bughub_templates/delete_post.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Your post has been deleted successfully!')
        return super().delete(request, *args, **kwargs)

class SearchView(generic.ListView):
    model = Post
    template_name = "bughub_templates/search_results.html"
    context_object_name = 'search_results'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Post.objects.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            ).order_by('-created_on')  # Removed status filter
        return Post.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        context['recent_posts'] = Post.objects.order_by("-created_on")  # Removed status filter
        return context

