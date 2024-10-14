# Defines the URL patterns for the accounts app, mapping views for user signup, login, logout,
# and password reset functionality to their corresponding routes.

from django.urls import path
from .views import (
    SignUpView, CustomLoginView, CustomLogoutView,
    PasswordResetRequestView, CustomPasswordResetDoneView
)

app_name = 'accounts'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('password_reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
]