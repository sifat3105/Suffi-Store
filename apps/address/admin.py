from django.contrib import admin
from apps.address.models import Address, PostalCode, ShippingCharge
from unfold.admin import ModelAdmin

# Register your models here.
@admin.register(Address)
class AddressAdmin(ModelAdmin):
    list_display = ('id', 'user', 'city', 'area', 'is_default', 'created_at')
    list_filter = ('is_default', 'city', 'area')
    search_fields = ('user__email', 'name', 'phone', 'city', 'area')

@admin.register(PostalCode)
class PostalCodeAdmin(ModelAdmin):
    list_display = ('id', 'code', 'city', 'area', 'is_available')
    list_filter = ('is_available', 'city', 'area')
    search_fields = ('code', 'city', 'area')

@admin.register(ShippingCharge)
class ShippingChargeAdmin(ModelAdmin):
    list_display = ('id', 'shipping_charge', 'description')
    search_fields = ('description',)