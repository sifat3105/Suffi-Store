from django.db import models
from django.contrib.auth import get_user_model
from apps.product.models import Product
from decimal import Decimal
from apps.address.models import Address

User = get_user_model()

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipping_charge = models.ForeignKey(
        'address.ShippingCharge',
        on_delete=models.SET_NULL,
        null=True,
        blank=True, default=0
    )

    @property
    def calculated_sub_total(self):
        return sum(
            (item.quantity * item.product.price for item in self.items.all()),
            Decimal('0.00')
        )

    @property
    def vat_percentage(self):
        from .models import VAT
        vat_obj = VAT.objects.filter(active=True).order_by('-updated_at').first()
        return vat_obj.percentage if vat_obj else Decimal('0.00')

    @property
    def calculated_vat(self):
        return (self.calculated_sub_total * self.vat_percentage) / Decimal('100')

    @property
    def shipping_charge_amount(self):
        if self.shipping_charge and hasattr(self.shipping_charge, 'shipping_charge'):
            return self.shipping_charge.shipping_charge or Decimal('0.00')
        return Decimal('0.00')

    @property
    def total_price(self):
        sub_total = self.calculated_sub_total if self.calculated_sub_total is not None else Decimal('0.00')
        shipping = self.shipping_charge_amount if self.shipping_charge_amount is not None else Decimal('0.00')
        vat = self.calculated_vat if self.calculated_vat is not None else Decimal('0.00')
        discount = self.discount if self.discount is not None else Decimal('0.00')
        return sub_total + shipping + vat - discount
    
class VAT(models.Model):
    percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"VAT: {self.percentage}%" 

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("cart", "product")

    def __str__(self):
        return f"{self.quantity} × {self.product.title}"

    @property
    def total_price(self):
        return self.quantity * self.product.price
    
class CouponCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code
    

class PaymentMethod(models.Model):
    CHOOICE_METHODS = [
        ('stripe', 'Stripe'),
        ('cod', 'Cash on Delivery'),
    ]
    name = models.CharField(max_length=100, choices=CHOOICE_METHODS, unique=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
