from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
User = get_user_model()


class PostalCode(models.Model):
    code = models.CharField(max_length=20, unique=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    area = models.CharField(max_length=100, blank=True, null=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.code} - {self.city} - {self.area}"

        

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    
    postal_code = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(10000), MaxValueValidator(99999)],
        help_text="Must be a 5-digit postal code."
    )
    city = models.CharField(max_length=100, blank=True, null=True)
    block_sector = models.CharField(max_length=100, blank=True, null=True)
    area = models.CharField(max_length=100, blank=True, null=True)
    street_road = models.CharField(max_length=100, blank=True, null=True)
    house_no = models.CharField(max_length=50, blank=True, null=True)
    flat_no = models.CharField(max_length=50, blank=True, null=True)
    floor_no = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    is_default = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    address_type = models.CharField(max_length=50, choices=[
        ('home', 'Home'),
        ('work', 'Work'),
        ('other', 'Other'),
    ], default='home')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_default', '-created_at']

    @property
    def is_available(self):
        return self.postal_code.is_available
    
class ShippingCharge(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False)
    shipping_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    description = models.CharField(max_length=255, blank=True, null=True)