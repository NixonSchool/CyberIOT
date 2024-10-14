# urls.py (in your app directory)
from django.urls import path
from . import views

app_name = 'settings'
urlpatterns = [
    path('settings/', views.settings_view, name='settings'),
]