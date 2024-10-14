from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from marketitem.models import Category, Item

from .forms import SignUpForm


# Create your views here.
def index(request):
    items = Item.objects.filter(status='available').order_by('-created_at')[
            :6]  # Display first six available items, sorted by newest first
    categories = Category.objects.all()

    return render(request, 'core/index.html', {
        'categories': categories,
        'items': items,
    })


def contact(request):
    return render(request, 'core/contact.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('/login/')
    else:
        form = SignUpForm()

    return render(request, 'core/signup.html', {
        'form': form,
    })


@login_required
def logout_user(request):
    logout(request)
    return redirect('marketdash:index')
