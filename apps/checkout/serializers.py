from apps.address.models import ShippingCharge
from rest_framework import serializers
from apps.cart.models import Cart
from decimal import Decimal

class DeliveryOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingCharge
        fields = ['id', 'name', 'description', 'shipping_charge']

class SelectDeliveryOptionSerializer(serializers.ModelSerializer):
    sub_total = serializers.SerializerMethodField()
    shipping_cost = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()
    discount = serializers.SerializerMethodField()

    class Meta:
        model = ShippingCharge
        fields = ['id', 'name', 'description', 'shipping_charge', 'sub_total', 'shipping_cost', 'discount', 'total']
    def get_sub_total(self, obj):
        """Get cart subtotal from the user's cart"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                cart = Cart.objects.get(user=request.user)
                return str(cart.sub_total)
            except Cart.DoesNotExist:
                return "0.00"
        return "0.00"

    def get_shipping_cost(self, obj):
        """Get selected delivery option price as shipping cost"""
        return str(obj.price)
    
    def get_discount(self, obj):
        """Get discount amount from the user's cart"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                cart = Cart.objects.get(user=request.user)
                return str(cart.discount)
            except Cart.DoesNotExist:
                return "0.00"
        return "0.00"

    def get_total(self, obj):
        """Calculate total = subtotal + shipping cost"""
        request = self.context.get('request')
        sub_total = Decimal('0.00')
        if request and request.user.is_authenticated:
            try:
                cart = Cart.objects.get(user=request.user)
                sub_total = cart.sub_total
            except Cart.DoesNotExist:
                pass
        shipping_cost = obj.price
        total = sub_total + shipping_cost - Decimal(self.get_discount(obj))
        return str(total)