from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from django.contrib.auth import get_user_model

User = get_user_model()


@login_required
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.profile
    is_owner_or_admin = (request.user == user) or request.user.is_staff
    context = {
        'profile': profile,
        'user': user,
        'is_owner_or_admin': is_owner_or_admin
    }
    return render(request, 'profiles/profile.html', context)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect(reverse('profiles:profile', kwargs={'username': request.user.username}))
    else:
        form = ProfileForm(instance=request.user.profile)

    context = {
        'form': form,
        'user': request.user
    }
    return render(request, 'profiles/edit_profile.html', context)