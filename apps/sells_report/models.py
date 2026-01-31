from django.db import models

# Create your models here.
class SellHistory(models.Model):
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    quantity_sold = models.PositiveIntegerField()
    sell_date = models.DateTimeField(auto_now_add=True)
    customer_name = models.CharField(max_length=100, blank=True,null=True)
    customer_email = models.EmailField()

    def __str__(self):
        return f"Sold {self.quantity_sold} of {self.product.title} on {self.sell_date}"