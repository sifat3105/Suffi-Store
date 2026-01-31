from django.db.models import Count
from apps.product.models import Product
from apps.product.serializers import ProductListSerializer

class CartUtils:
    def get_enhanced_related_products(self, cart):
        """
        Get related products using multiple strategies
        """
        if not cart.items.exists():
            return self.get_popular_products()  # Fallback to popular products
        
        cart_product_ids = [item.product.id for item in cart.items.all()]
        
        # Strategy 1: Same category products
        category_products = self.get_products_by_category(cart, cart_product_ids)
        
        # Strategy 2: Frequently bought together (if you have order data)
        frequently_bought_products = self.get_frequently_bought_together(cart_product_ids)
        
        # Combine and deduplicate results
        all_related_ids = set()
        related_products = []
        
        # Add category-based products
        for product_data in category_products[:6]:  # Take up to 6 from categories
            if product_data['id'] not in all_related_ids:
                related_products.append(product_data)
                all_related_ids.add(product_data['id'])
        
        # Add frequently bought together products
        for product_data in frequently_bought_products[:4]:  # Take up to 4 from frequently bought
            if product_data['id'] not in all_related_ids and len(related_products) < 10:
                related_products.append(product_data)
                all_related_ids.add(product_data['id'])
        
        return related_products

    def get_products_by_category(self, cart, cart_product_ids):
        """Get products from same categories as cart items"""
        cart_categories = set()
        for item in cart.items.all():
            if item.product.category:
                cart_categories.add(item.product.category)
        
        if not cart_categories:
            return []
        
        products = Product.objects.filter(
            category__in=cart_categories
        ).exclude(
            id__in=cart_product_ids
        ).select_related('category').order_by('-created_at')[:15]
        
        return ProductListSerializer(products, many=True).data

    def get_frequently_bought_together(self, cart_product_ids):
        
        cart_products = Product.objects.filter(id__in=cart_product_ids)
        cart_categories = set(product.category for product in cart_products if product.category)
        
        if not cart_categories:
            return []
        frequently_bought = Product.objects.filter(
            category__in=cart_categories
        ).exclude(
            id__in=cart_product_ids
        ).annotate(
            order_count=Count('order_items')
        ).order_by('-order_count')[:10]

        return ProductListSerializer(frequently_bought, many=True).data

    def get_popular_products(self):
        """Fallback to popular products when cart is empty"""
        popular_products = Product.objects.annotate(
            order_count=Count('order_items')
        ).order_by('-order_count')[:10]
        
        
        
        return ProductListSerializer(popular_products, many=True).data