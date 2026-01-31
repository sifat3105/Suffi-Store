from django.db import models
from apps.user.manager import UserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_login = models.DateTimeField(null=True, blank=True, default=None)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    def __str__(self):
        return self.email


    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, if admin
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, if admin
        return self.is_admin
    
class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    profile_image = models.ImageField(upload_to='users/', blank=True)
    last_login = models.DateTimeField(null=True, blank=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.name}"
    
class UserOtp(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    token = models.CharField(max_length=255,unique=True)
    otp = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

class LoginHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='login_history')
    device = models.CharField(max_length=255, blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    login_time = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-login_time']

    def __str__(self):
        return f"{self.user.email} - {self.device or 'Unknown Device'}"
    

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')

    def __str__(self):
        return f"Wishlist of {self.user.email}"
    
class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name='items')
    product_id = models.PositiveIntegerField()

    class Meta:
        unique_together = ['wishlist', 'product_id']

    def __str__(self):
        return f"Product {self.product_id} in {self.wishlist.user.email}'s wishlist"
    
class RecentlyViewedProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recently_viewed_products')
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-viewed_at']
        unique_together = ['user', 'product']

    def __str__(self):
        return f"Product {self.product.id} viewed by {self.user.email} at {self.viewed_at}"
