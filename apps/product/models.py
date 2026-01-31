from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.template.defaultfilters import slugify
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from django.utils.crypto import get_random_string

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slogan = models.CharField(max_length=100, blank=True)
    icon = models.ImageField(upload_to='categories/', blank=True)
    svg_icon = models.TextField(blank=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name



class Product(models.Model):

    STOCK_STATUS_CHOICES = [
        ('in-stock', 'In Stock'),
        ('low-stock', 'Low Stock'),
        ('out-of-stock', 'Out of Stock'),
        ('discontinued', 'Discontinued'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    about_product = models.TextField(blank=True)

    quantity = models.PositiveIntegerField(default=0)

    old_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)

    unit = models.CharField(max_length=20, default='kg')
    badge = models.CharField(max_length=50, blank=True)

    rating = models.FloatField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )

    stock_status = models.CharField(
        max_length=20,
        choices=STOCK_STATUS_CHOICES,
        default='in-stock'
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        null=True,
        blank=True
    )

    brand = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # ---------- SLUG ----------
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{get_random_string(4)}"
            self.slug = slug

        # ---------- STOCK STATUS ----------
        if self.stock_status != 'discontinued':
            self.stock_status = self.compute_stock_status()

        super().save(*args, **kwargs)


    def compute_stock_status(self):
        if self.stock_status == 'discontinued':
            return 'discontinued'
        if self.quantity > 10:
            return 'in-stock'
        if self.quantity > 0:
            return 'low-stock'
        return 'out-of-stock'


    @property
    def discount_percentage(self):
        if self.old_price and self.old_price > self.price:
            return int(((self.old_price - self.price) / self.old_price) * 100)
        return 0

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=100, blank=True)
    is_primary = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"Image for {self.product.title}"

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class ProductTag(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_tags')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['product', 'tag']

    def __str__(self):
        return f"{self.product.title} - {self.tag.name}"
    

    
class WeeklySpecialProduct(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='weekly_special_products'
    )
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        ordering = ['order']  # default sorting

    def __str__(self):
        return f"{self.product.title} ({self.start_date} → {self.end_date})"
    

# class Review(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
#     user_name = models.CharField(max_length=100)
#     rating = models.IntegerField(
#         validators=[MinValueValidator(1), MaxValueValidator(5)]
#     )
#     comment = models.TextField()
#     is_approved = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ['-created_at']

#     def __str__(self):
#         return f"Review for {self.product.title} by {self.user_name}"
