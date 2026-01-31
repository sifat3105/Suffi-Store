from django.db import models
from django.contrib.auth import get_user_model
from apps.product.models import Product

User = get_user_model()

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=100, unique=True)
    tracking_id = models.CharField(max_length=100, unique=True)
    products = models.ManyToManyField(Product, through="OrderItem", related_name="orders")
    products_name = models.CharField(max_length=1024, blank=True, null=True, help_text="Comma-separated product names for this order.")
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipping_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    vat_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    status = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('in_shipping', 'In Shipping'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], default='pending')
    payment_status = models.CharField(max_length=50, choices=[
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid'),
        ('refunded', 'Refunded'),
    ], default='unpaid')
    is_paid = models.BooleanField(default=False)
    placed_on = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} for {self.user.email}"
    
    # def calculate_vat_charge(self):
    #     vat_amount = (self.total_price * 15) / 100
    #     self.vat_charge = vat_amount
    #     self.save()
    #     return vat_amount

    # def calculate_total_price(self):
    #     self.total_price = self.sub_total + self.shipping_charge + self.vat_amount - self.discount
    #     self.save()
    #     return self.total_price


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order_items")
    quantity = models.PositiveIntegerField(default=1)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)

    def product_name(self):
        return self.product.title if self.product else ""
    product_name.short_description = 'Product Name'

    def __str__(self):
        return f"{self.quantity} x {self.product.title if self.product else ''} in Order #{self.order.id}"
