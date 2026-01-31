from django.db import models
from django.contrib.auth import get_user_model
from apps.product.models import Product

User = get_user_model()

class   Review(models.Model):
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True) 
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at'] 

    def __str__(self):
        return f"Review by {self.reviewer} for {self.product.title}"
    


class ContactUs(models.Model):
    name = models.CharField(max_length=100,null=False, blank=False)
    email = models.EmailField(null=False, blank=False)
    subject = models.CharField(max_length=200,null=False, blank=False)
    message = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Contact Us Message from {self.name} - {self.subject}"