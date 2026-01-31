from django.db import models
from django.contrib.auth import get_user_model
from apps.product.models import Product

User = get_user_model()

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'product']

    def __str__(self):
        # Use get_username() to support custom User models (USERNAME_FIELD may be email)
        try:
            username = self.user.get_username()
        except Exception:
            username = getattr(self.user, 'email', str(self.user))
        return f"{username} favorites {self.product.title}"