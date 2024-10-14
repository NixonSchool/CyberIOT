from django.contrib import admin
from .models import Category, Item, Order, Comment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'quantity', 'status', 'created_by', 'created_at')
    list_filter = ('category', 'status', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at',)
    raw_id_fields = ('created_by',)
    date_hierarchy = 'created_at'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'payment_method', 'is_paid', 'is_cancelled', 'created_at')
    list_filter = ('payment_method', 'is_paid', 'is_cancelled', 'created_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at',)
    raw_id_fields = ('user', 'items')
    date_hierarchy = 'created_at'

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('items')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'item__name', 'content')
    readonly_fields = ('created_at',)
    raw_id_fields = ('user', 'item')
    date_hierarchy = 'created_at'