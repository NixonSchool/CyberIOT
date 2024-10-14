from django.urls import path
from . import views

app_name = 'forum_search'

urlpatterns = [
    path('', views.search_view, name='search'),
]