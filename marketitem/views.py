from django.contrib.auth.decorators import login_required
from django.db.models import Q, Avg
from django.shortcuts import render, get_object_or_404, redirect
from .forms import NewItemForm, EditItemForm, CommentForm, CreditCardForm
from .models import Item, Category, Order, Comment
from decimal import Decimal
from django.utils import timezone
from django.contrib import messages


def items(request):
    items = Item.objects.all()
    category_id = request.GET.get('category', 0)
    categories = Category.objects.all()
    query = request.GET.get('query', '')

    if category_id:
        items = items.filter(category_id=category_id)
    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))

    return render(request, 'item/items.html', {
        'items': items,
        'query': query,
        'categories': categories,
        'category_id': int(category_id),
    })


def decrease_quantity(self, amount=1):
    if self.quantity >= amount:
        self.quantity -= amount
        if self.quantity == 0:
            self.status = 'sold_out'
        self.save()
        return True
    return False


def increase_quantity(self, amount=1):
    self.quantity += amount
    if self.status == 'sold_out':
        self.status = 'available'
    self.save()


@login_required
def new(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()
            return redirect('marketitem:detail', pk=item.id)
    else:
        form = NewItemForm()

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'New Item',
    })


@login_required
def edit(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('marketitem:detail', pk=item.id)
    else:
        form = EditItemForm(instance=item)

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'Edit Item',
    })



@login_required
def delete(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    item.delete()

    return redirect('marketdash:index')


def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, status='available').exclude(pk=pk)[0:3]
    comments = item.comments.all()
    average_rating = comments.aggregate(Avg('rating'))['rating__avg']

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.item = item
            comment.user = request.user
            comment.save()
            return redirect('marketitem:detail', pk=pk)
    else:
        form = CommentForm()

    return render(request, 'item/detail.html', {
        'item': item,
        'related_items': related_items,
        'comments': comments,
        'average_rating': average_rating,
        'form': form,
    })

@login_required
def checkout_failed(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    return render(request, 'item/checkout_failed.html', {'item': item})


@login_required
def checkout(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if not item.is_available():
        return redirect('marketitem:detail', pk=item.id)

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')

        if payment_method == 'credit_card':
            form = CreditCardForm(request.POST)
            if not form.is_valid():
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field.capitalize()}: {error}")
                return render(request, 'item/checkout.html', {'item': item, 'form': form})

        order = Order.objects.create(
            user=request.user,
            total_price=item.price,
            payment_method=payment_method
        )
        order.items.add(item)

        if payment_method == 'paypal':
            order.paypal_email = request.POST.get('paypal_email')
        elif payment_method == 'credit_card':
            order.card_number = f"****-****-****-{form.cleaned_data['card_number'][-4:]}"
            order.card_expiry = form.cleaned_data['expiry_date']

        # Simulate payment process
        import time
        import random
        time.sleep(2)  # Simulate processing delay
        if random.random() < 0.9:  # 90% success rate
            order.is_paid = True
            order.save()

            # Decrease item quantity
            if item.decrease_quantity():
                messages.success(request,
                                 "Purchase successful! An email has been sent with the checkout details and contact information.")
                return redirect('marketitem:order_confirmation', order_id=order.id)
            else:
                messages.error(request, "Sorry, this item is no longer available.")
                order.delete()
                return redirect('marketitem:detail', pk=item.id)
        else:
            # Payment failed
            order.delete()
            return redirect('marketitem:checkout_failed', item_id=item.id)

    form = CreditCardForm()
    return render(request, 'item/checkout.html', {'item': item, 'form': form})

@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    can_cancel = (timezone.now() - order.created_at).days < 1

    if request.method == 'POST' and can_cancel:
        # Cancel the order
        order.cancel()
        messages.success(request, "Your order has been cancelled successfully.")
        return redirect('marketitem:order_cancelled', order_id=order.id)

    return render(request, 'item/order_confirmation.html', {
        'order': order,
        'can_cancel': can_cancel,
    })


@login_required
def order_cancelled(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user, is_cancelled=True)
    return render(request, 'item/order_cancelled.html', {'order': order})