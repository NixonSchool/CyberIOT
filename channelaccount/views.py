from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from video.models import Video
from channel.models import Channel
from .forms import UserUpdateForm, ChangeUserPasswordForm

User = get_user_model()


# Redirect to the login page from the accounts app
def loginView(request):
    return redirect('accounts:login')

# Redirect to the signup page from the accounts app
def signUp(request):
    return redirect('accounts:signup')

# Use the accounts app logout view
@login_required
def logoutView(request):
    return redirect('accounts:logout')


@login_required
def userProfile(request):
    if Channel.objects.filter(user_id=request.user.id).exists():
        channel = Channel.objects.get(user=request.user.id)
        context = {
            'channel': channel,
            'total_videos': Video.objects.filter(channel_id=channel.id, user_id=request.user.id).count(),
        }
        return render(request, 'account/user/profile.html', context)
    context = {}
    return render(request, 'account/user/profile.html', context)


@login_required
def updateUserProfile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your Profile has been updated!')
            return redirect('channelaccount:userProfile')
        else:
            return render(request, 'account/update_profile.html', {'form': user_form})

    user_form = UserUpdateForm(instance=request.user)
    return render(request, 'account/update_profile.html', {'form': user_form})


@login_required
def changeUserPassword(request):
    form = ChangeUserPasswordForm(data=request.POST, user=request.user)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            user = authenticate(request, username=request.user.username, password=form.cleaned_data['new_password2'])
            login(request, user)
            messages.success(request, 'Your password has been successfully updated.')

            return redirect("accounts:password_reset_request")

    context = {
        'form': form
    }
    return redirect("accounts:password_reset_request")