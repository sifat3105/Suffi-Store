from rest_framework import serializers

from apps.user.models import RecentlyViewedProduct
from .models import Product, ProductImage, Tag, ProductTag, Category
from apps.review.serializers import ReviewSerializer
from apps.favorite.models import Favorite

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image', 'alt_text', 'is_primary']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']


class ProductSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many=True, read_only=True)
    discount_percentage = serializers.ReadOnlyField()
    is_favorite = serializers.SerializerMethodField()
    stock_status = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'title', 'description', 'images', 'tags',
            'badge', 'old_price', 'quantity', 'price', 'unit', 'stock_status', 'rating', 'reviews',
            'discount_percentage', 'is_favorite', 'about_product'
        ]

    def get_is_favorite(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            prefetched = getattr(obj, '_prefetched_objects_cache', None) or {}
            if 'favorite_set' in prefetched:
                user = request.user
                return any(f.user_id == user.id for f in obj.favorite_set.all())
            return obj.favorite_set.filter(user=request.user).exists()
        return False
    
    def get_images(self, obj):
        images = getattr(obj, 'prefetched_images', None)
        if images is None:
            images = obj.images.all().order_by('order')

        if images:
            return [self._get_image_url(image.image) for image in images]
        return ["/images/card-img.jpg"] * 3

    def _get_image_url(self,  image_field):
        request = self.context.get('request')
        """Return absolute URL for an ImageField (with fallback)."""
        if image_field and hasattr(image_field, 'url'):
            return request.build_absolute_uri(image_field.url) if request else image_field.url
        return request.build_absolute_uri("/images/card-img.jpg")

    def get_tags(self, obj):
        prefetched = getattr(obj, 'prefetched_tags', None)
        if prefetched is not None:
            return [t.name for t in prefetched]

        product_tags = obj.product_tags.all()
        if product_tags:
            return [pt.tag.name for pt in product_tags]
        return []

    def get_stock_status(self, obj):
        return obj.compute_stock_status()

    

class ProductListSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    oldPrice = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    isFavorite = serializers.SerializerMethodField()
    stockStatus = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'title', 'description', 'images', 'tags', 
            'badge', 'rating', 'oldPrice', 'price', 'unit', 
            'stockStatus', 'isFavorite'
        ]

    def get_images(self, obj):
        images = getattr(obj, 'prefetched_images', None)
        if images is None:
            images = obj.images.all().order_by('order')

        if images:
            return [self._get_image_url(image.image) for image in images]
        return ["/images/card-img.jpg"] * 3

    def _get_image_url(self, image_field):
        """Extract relative URL from ImageField"""
        if image_field and hasattr(image_field, 'url'):
            return image_field.url
        return "/images/card-img.jpg"

    def get_tags(self, obj):
        prefetched = getattr(obj, 'prefetched_tags', None)
        if prefetched is not None:
            return [t.name for t in prefetched]

        product_tags = obj.product_tags.all()
        if product_tags:
            return [pt.tag.name for pt in product_tags]
        return []

    def get_oldPrice(self, obj):
        return str(obj.old_price) if obj.old_price else None

    def get_price(self, obj):
        return str(obj.price)

    def get_isFavorite(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            prefetched = getattr(obj, 'prefetched_favorites', None)
            if prefetched is not None:
                return len(prefetched) > 0

            # Fallback to a DB query
            return Favorite.objects.filter(
                user=request.user,
                product=obj
            ).exists()
        return False

    def get_stockStatus(self, obj):
        return obj.compute_stock_status()
    

class CategorySerializer(serializers.ModelSerializer):
    icon = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = ['name', 'slogan']

    def get_icon(self, obj):
        if obj.svg_icon:
            return obj.svg_icon
        return obj.icon.url
    
class RecentlyViewedProductSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)

    class Meta:
        model = RecentlyViewedProduct
        fields = ['product']