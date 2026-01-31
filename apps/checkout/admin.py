from django.contrib import admin
from apps.address.models import ShippingCharge
from unfold.admin import ModelAdmin

# # Register your models here.
# @admin.register(DeliveryOption)
# class DeliveryOptionAdmin(ModelAdmin):
#     list_display = ('id', 'name', 'price')
#     search_fields = ('name',)
#     list_filter = ('price',)