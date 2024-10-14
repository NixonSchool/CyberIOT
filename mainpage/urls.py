# mainpage/urls.py
from django.urls import path
from .views import main_page

app_name = 'mainpage'

urlpatterns = [
    path('', main_page, name='main_page'),  # URL for the main page
]
