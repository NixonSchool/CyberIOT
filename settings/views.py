import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ChangePasswordForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import UserSettings


@login_required
def settings_view(request):
    # Get or create user settings
    user_settings, created = UserSettings.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        if 'save_settings' in request.POST:
            # Process the settings form
            user_settings.email_notifications = 'email_notifications' in request.POST
            user_settings.in_app_notifications = 'in_app_notifications' in request.POST
            user_settings.dark_mode = 'dark_mode' in request.POST
            user_settings.sound_effects = 'sound_effects' in request.POST
            user_settings.auto_update = 'auto_update' in request.POST
            user_settings.data_usage = 'data_usage' in request.POST
            user_settings.location_services = 'location_services' in request.POST
            user_settings.save()
            messages.success(request, 'Settings saved successfully!')

        elif 'reset_defaults' in request.POST:
            # Reset settings to defaults
            user_settings.reset_to_defaults()  # Implement this method in your model
            messages.info(request, 'Settings reset to defaults.')

        elif 'change_password' in request.POST:
            form = ChangePasswordForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                # Send password reset email logic here
                messages.info(request, f'Password reset email sent to {email}')
            else:
                messages.error(request, 'Invalid email address.')

    else:
        form = ChangePasswordForm()

    return render(request, 'settings/settings.html', {'settings': user_settings, 'form': form})

@csrf_exempt
def save_dark_mode(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        dark_mode = data.get('dark_mode', False)

        # Get or create user settings
        user_settings, created = UserSettings.objects.get_or_create(user=request.user)

        # Update the user settings
        user_settings.dark_mode = dark_mode
        user_settings.save()

        return JsonResponse({'status': 'success'})