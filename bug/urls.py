from django.urls import path
from . import views
from .feeds import AtomSiteNewsFeed, LatestPostsFeed
from .views import DeletePost

app_name = 'bug'

urlpatterns = [
    path("feed/rss", LatestPostsFeed(), name="post_feed"),
    path("feed/atom", AtomSiteNewsFeed(), name="atom_feed"),
    path("blog/", views.PostList.as_view(), name="home"),
    path("blog/add/", views.AddPost.as_view(), name="add_post"),
    path("blog/<slug:slug>/", views.PostDetail.as_view(), name="post_detail"),
    path("blog/<slug:slug>/edit/", views.EditPost.as_view(), name="edit_post"),  # New URL pattern
    path('search/', views.SearchView.as_view(), name='search'),
    path('api/latest-post/', views.latest_post, name='latest_post'),
    path('delete/<slug:slug>/', DeletePost.as_view(), name='delete_post'),

]