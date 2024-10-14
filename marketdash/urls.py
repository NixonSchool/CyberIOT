from django.urls import path

from . import views

app_name = 'marketdash'

urlpatterns = [
  path('', views.index, name='index'),
]
