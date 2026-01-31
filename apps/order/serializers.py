from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    product_price = serializers.SerializerMethodField()
    class Meta:
        model = OrderItem
        fields = ['id', 'product_name', 'quantity', 'product_price']

    def get_product_price(self, obj):
        return obj.product_price

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    shipping_charge = serializers.SerializerMethodField()
    vat_amount = serializers.SerializerMethodField()
    discount = serializers.SerializerMethodField()
    sub_total = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'order_id', 'tracking_id', 'status', 'is_paid', 'placed_on', 'sub_total', 'shipping_charge', 'vat_amount', 'discount', 'total_price','items']

    def get_total_price(self, obj):
        print("Calculating total price for order:", obj.sub_total + obj.shipping_charge + obj.vat_amount - obj.discount)
        return obj.sub_total + obj.shipping_charge + obj.vat_amount - obj.discount
    
    def get_shipping_charge(self, obj):
        return obj.shipping_charge
    
    def get_sub_total(self, obj):
        return obj.sub_total
    
    def get_vat_amount(self, obj):
        return obj.vat_amount
    
    def get_discount(self, obj):
        return obj.discount