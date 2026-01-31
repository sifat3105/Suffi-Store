from django.contrib import admin
from unfold.admin import ModelAdmin
from apps.cart.models import Cart, CartItem, CouponCode

# Register your models here.
@admin.register(Cart)
class CartAdmin(ModelAdmin):
    list_display = ('id', 'user', 'calculated_sub_total', 'shipping_charge', 'calculated_vat', 'discount', 'total_price')
    search_fields = ('user__email',)
    # reduce queries by selecting related user when rendering changelist/detail
    list_select_related = ('user',)
    
@admin.register(CartItem)
class CartItemAdmin(ModelAdmin):
    list_display = ('id', 'cart', 'product', 'quantity', 'created_at')
    # select related cart and product to avoid extra queries in admin list
    list_select_related = ('cart', 'product', 'cart__user')
    search_fields = ('cart__user__email', 'product__title')
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('total_price',)
    def total_price(self, obj):
        return obj.total_price
    total_price.short_description = 'Total Price'    
    ordering = ('-product__price',)

@admin.register(CouponCode)
class CouponCodeAdmin(ModelAdmin):
    list_display = ('id', 'code', 'discount_percentage', 'active', 'created_at')
    search_fields = ('code',)
    list_filter = ('active', 'created_at', 'updated_at')
    ordering = ('-created_at',)