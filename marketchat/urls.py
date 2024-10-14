from django.urls import path
from . import views

app_name = 'marketchat'

urlpatterns = [
    # Main chat views
    path('', views.inbox, name='inbox'),
    path('<int:pk>/', views.detail, name='detail'),
    path('new/<int:item_pk>/', views.new_conversation, name='new'),

    # API endpoints for notifications
    path('unread-count/', views.get_unread_message_count, name='unread_count'),
]