from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Item(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('sold_out', 'Sold Out'),
        ('coming_soon', 'Coming Soon'),
        ('unavailable', 'Currently Unavailable'),
        ('subscription', 'Monthly Subscription'),
    ]

    category = models.ForeignKey('Category', related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()  # This is the one-time purchase price
    monthly_price = models.FloatField(null=True, blank=True)  # For subscription models
    image = models.ImageField(upload_to='item_images', blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='items_created', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    available_from = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    def is_available(self):
        return self.status == 'available' and self.quantity > 0 and (
                    self.available_from is None or self.available_from <= timezone.now())

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

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=20, choices=[
        ('paypal', 'PayPal'),
        ('credit_card', 'Credit Card'),
    ])
    is_paid = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)

    # Payment information fields
    paypal_email = models.EmailField(blank=True, null=True)
    card_number = models.CharField(max_length=16, blank=True, null=True)
    card_expiry = models.CharField(max_length=5, blank=True, null=True)
    card_cvv = models.CharField(max_length=4, blank=True, null=True)

    def cancel(self):
        if not self.is_cancelled:
            self.is_cancelled = True
            for item in self.items.all():
                item.increase_quantity()
            self.save()

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"


class Comment(models.Model):
    item = models.ForeignKey(Item, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Comment by {self.user.username} on {self.item.name}'