from django.contrib import admin
from unfold.admin import ModelAdmin
from apps.order.models import Order, OrderItem

# Register your models here.
@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'status')
    search_fields = ('user__email',)
    ordering = ('-created_at',)

@admin.register(OrderItem)
class OrderItemAdmin(ModelAdmin):
    list_display = ('id', 'order', 'product_name', 'quantity')
    search_fields = ('order__user__email', 'product__name')
