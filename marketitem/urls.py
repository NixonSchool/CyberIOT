from django.urls import path

from . import views

app_name = 'marketitem'

urlpatterns = [
    path('', views.items, name='items'),
    path('new/', views.new, name='new'),
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('<int:pk>/edit/', views.edit, name='edit'),
    path('checkout/<int:item_id>/', views.checkout, name='checkout'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('order-cancelled/<int:order_id>/', views.order_cancelled, name='order_cancelled'),
    path('checkout-failed/<int:item_id>/', views.checkout_failed, name='checkout_failed'),  # New URL pattern
]