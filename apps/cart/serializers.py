from rest_framework import serializers
from .models import Cart, CartItem
from apps.product.serializers import ProductListSerializer
from decimal import Decimal


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.title', read_only=True)
    product_id = serializers.IntegerField(source='product.id', read_only=True)
    price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)
    sku = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'product_name', 'sku', 'image', 'price', 'quantity']

    def get_sku(self, obj):
        return f"{obj.product.title[:4].upper()} •XCCZ"

    def get_image(self, obj):
        image = obj.product.images.filter(is_primary=True).first()
        if not image:
            image = obj.product.images.first()
        if image:
            return image.image.url
        return None


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    sub_total = serializers.SerializerMethodField()
    shipping_fee = serializers.SerializerMethodField()
    vat = serializers.SerializerMethodField()
    discount = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['items', 'sub_total', 'shipping_fee', 'vat', 'discount', 'total_price']

    def get_shipping_fee(self, obj):
        """Shipping charge from related ShippingCharge model"""
        if obj.shipping_charge:
            return obj.shipping_charge.shipping_charge
        return Decimal('0.00')

    def get_sub_total(self, obj):
        return obj.calculated_sub_total
    
    def get_vat(self, obj):
        return obj.calculated_vat
    
    def get_discount(self, obj):
        return obj.discount

    def get_total_price(self, obj):
        return obj.total_price