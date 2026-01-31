from rest_framework.views import APIView
from rest_framework import status, generics, filters, permissions
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from apps.user.models import RecentlyViewedProduct
from .models import Product, WeeklySpecialProduct, ProductImage, Tag
from apps.favorite.models import Favorite
from django.db.models import Prefetch
from django.db.models import Prefetch, Min, Max, Count
from .serializers import ProductSerializer, ProductListSerializer, RecentlyViewedProductSerializer
from apps.common.response import custom_response
from apps.common.pagination import CustomPagination
from django.utils import timezone
from apps.product.utils import get_recently_viewed_products, get_best_selling_products, get_weekly_special_products
from apps.review.models import Review
from apps.review.serializers import ReviewSerializer

class ProductListView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    pagination_class = CustomPagination
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'rating', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True).prefetch_related(
            Prefetch('images', queryset=ProductImage.objects.order_by('order'), to_attr='prefetched_images'),
            'product_tags__tag',
            'favorite_set'
        )

        stock_status = self.request.query_params.get('stock_status')
        if stock_status:
            queryset = queryset.filter(stock_status=stock_status)

        categories = self.request.query_params.get('categories')
        if categories:
            category_list = [cat.strip() for cat in categories.split(',')]
            queryset = queryset.filter(category__name__in=category_list).distinct()
        
        brands = self.request.query_params.get('brands')
        if brands:
            brand_list = [brand.strip() for brand in brands.split(',')]
            queryset = queryset.filter(brand__in=brand_list).distinct()

        price_min = self.request.query_params.get('price_min')
        price_max = self.request.query_params.get('price_max')
        if price_min or price_max:
            if price_min and price_max:
                queryset = queryset.filter(price__gte=price_min, price__lte=price_max)
            elif price_min:
                queryset = queryset.filter(price__gte=price_min)
            elif price_max:
                queryset = queryset.filter(price__lte=price_max)
        
        rating = self.request.query_params.get('rating')
        if rating:
            try:
                rating_value = float(rating)
                queryset = queryset.filter(rating__gte=rating_value)
            except (ValueError, TypeError):
                pass

        dietary = self.request.query_params.get('dietary')
        if dietary:
            dietary_list = [diet.strip() for diet in dietary.split(',')]
            queryset = queryset.filter(product_tags__tag__name__in=dietary_list).distinct()
        
        in_stock = self.request.query_params.get('in_stock')
        if in_stock and in_stock.lower() == 'true':
            queryset = queryset.filter(stock_status='in-stock')
        
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        
        return custom_response(
            status="success",
            status_code=status.HTTP_200_OK,
            message="Product retrieved successfully",
            data=serializer.data
        )
        
    

class ProductDetailView(APIView):
    def get(self, request, pk):
        authenticated = request.user.is_authenticated
        print("Authenticated:", authenticated)
        if authenticated:
            product = Product.objects.get(id=pk)
            # Create or update
            obj, created = RecentlyViewedProduct.objects.update_or_create(
                user=request.user, product=product
            )

            # Keep only last 10
            recent_ids = (
                RecentlyViewedProduct.objects
                .filter(user=request.user)
                .order_by('-viewed_at')
                .values_list('id', flat=True)[:10]
            )
            # Delete older ones
            RecentlyViewedProduct.objects.filter(user=request.user).exclude(id__in=recent_ids).delete()
        try:
            product = (
                Product.objects
                .prefetch_related(
                    "reviews",
                    Prefetch('images', queryset=ProductImage.objects.order_by('order'), to_attr='prefetched_images')
                )
                .get(pk=pk)
            )
        except Product.DoesNotExist:
            return custom_response(
                status="error",
                status_code=status.HTTP_404_NOT_FOUND,
                message="Product not found",
                data=None
            )
        self._add_to_recently_viewed(request, product)
        serializer = ProductSerializer(product)
        
        
        return custom_response(
            status="success",
            status_code=status.HTTP_200_OK,
            message="Product retrieved successfully",
            data={
            "product": serializer.data,
            }
        )
    
    def _add_to_recently_viewed(self, request, product):
        """
        Add product to recently viewed items in session
        """
        if 'recently_viewed' not in request.session:
            request.session['recently_viewed'] = []

        recently_viewed = request.session['recently_viewed']
        recently_viewed = [item for item in recently_viewed if item['id'] != product.id]
        
        # use prefetched_images if available to avoid extra DB queries
        image_url = None
        prefetched = getattr(product, 'prefetched_images', None)
        if prefetched:
            first_image = prefetched[0] if len(prefetched) > 0 else None
            image_url = first_image.image.url if first_image and first_image.image else None
        else:
            image_url = product.images.first().image.url if product.images.exists() else None

        product_data = {
            'id': product.id,
            'title': product.title,
            'price': str(product.price),
            'image': image_url,
            'viewed_at': timezone.now().isoformat()
        }
        
        recently_viewed.insert(0, product_data)
        recently_viewed = recently_viewed[:10]
        
        request.session['recently_viewed'] = recently_viewed
        request.session.modified = True


class ProductFiltersView(APIView):
    """
    Return metadata needed to render the filters on the frontend.

    Response shape (data): {
        categories: ["Vegetable", ...],
        brands: ["Pran", ...],
        price: { min: "0.00", max: "500.00" },
        dietary_tags: ["Sugar-Free", ...],
        has_in_stock: true
    }
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        try:
            active_products = Product.objects.filter(is_active=True)

            # Categories present in active products
            categories = (
                active_products
                .filter(category__isnull=False)
                .values_list('category__name', flat=True)
                .distinct()
            )

            # Brands (exclude blank/empty)
            brands = (
                active_products
                .exclude(brand__isnull=True)
                .exclude(brand__exact='')
                .values_list('brand', flat=True)
                .distinct()
            )

            # Price range
            price_agg = active_products.aggregate(min_price=Min('price'), max_price=Max('price'))
            min_price = price_agg.get('min_price') or 0
            max_price = price_agg.get('max_price') or 0

            # Dietary tags
            dietary_tags = (
                Tag.objects
                .filter(producttag__product__is_active=True)
                .values_list('name', flat=True)
                .distinct()
            )

            # Availability
            in_stock_count = active_products.filter(stock_status='in-stock').count()
            has_in_stock = in_stock_count > 0

            data = {
                'categories': list(categories),
                'brands': list(brands),
                'price': {
                    'min': str(min_price),
                    'max': str(max_price)
                },
                'dietary_tags': list(dietary_tags),
                'has_in_stock': has_in_stock
            }

            return custom_response(
                status="success",
                status_code=status.HTTP_200_OK,
                message="Filter metadata retrieved successfully",
                data=data
            )

        except Exception as e:
            return custom_response(
                status="error",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="An error occurred while retrieving filter metadata",
                data=str(e)
            )



class WeeklySpecialProductView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        try:
            today = timezone.now().date()
            weekly_specials = WeeklySpecialProduct.objects.filter(
                start_date__lte=today,
                end_date__gte=today
            ).prefetch_related(
                Prefetch('product__images', queryset=ProductImage.objects.order_by('order'), to_attr='prefetched_images')
            )
            products = [special.product for special in weekly_specials]
            serializer = ProductListSerializer(products, many=True, context={'request': request})
            return custom_response(
                status="success",
                status_code=status.HTTP_200_OK,
                message="Weekly special products retrieved successfully",
                data=serializer.data
            )
        except Exception as e:
            return custom_response(
                status="error",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="An error occurred while retrieving weekly special products",
                data=str(e)
            )
        

class BestSellingProductView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        try:
            best_selling_products = get_best_selling_products()
            serializer = ProductListSerializer(best_selling_products, many=True, context={'request': request})
            return custom_response(
                status="success",
                status_code=status.HTTP_200_OK,
                message="Best selling products retrieved successfully",
                data=serializer.data
            )
        except Exception as e:
            return custom_response(
                status="error",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="An error occurred while retrieving best selling products",
                data=str(e)
            )
        



class HomePageDataView(APIView):

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        try:
            today = timezone.now().date()
            
            weekly_special_products = get_weekly_special_products()
            weekly_serializer = ProductListSerializer(
                weekly_special_products, many=True, context={'request': request}
            )
            
            best_selling_products = get_best_selling_products()
            best_selling_serializer = ProductListSerializer(
                best_selling_products, many=True, context={'request': request}
            )
            
            recent_reviews = Review.objects.filter(is_approved=True).order_by('-rating')[:5]
            review_serializer = ReviewSerializer(recent_reviews, many=True)
            
            data = {
                "weekly_special_products": weekly_serializer.data,
                "best_selling_products": best_selling_serializer.data,
                "recent_reviews": review_serializer.data
            }

            return custom_response(
                status="success",
                status_code=status.HTTP_200_OK,
                message="Home page data retrieved successfully",
                data=data
            )
        
        except Exception as e:
            return custom_response(
                status="error",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="An error occurred while retrieving home page data",
                data=str(e)
            )
    

class RecentlyViewedProductView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            recent_qs = (
                RecentlyViewedProduct.objects
                .filter(user=request.user)
                .select_related('product')  # one-to-one fetch
                .prefetch_related(
                    Prefetch(
                        'product__images',
                        queryset=ProductImage.objects.only('id', 'image', 'product', 'order').order_by('order'),
                        to_attr='prefetched_images'
                    ),
                    Prefetch(
                        'product__product_tags__tag',
                        queryset=Tag.objects.only('id', 'name'),
                        to_attr='prefetched_tags'
                    ),
                    Prefetch(
                        'product__favorite_set',
                        queryset=Favorite.objects.filter(user=request.user).only('id', 'product', 'user'),
                        to_attr='prefetched_favorites'
                    )
                )
                .order_by('-viewed_at')[:10]
            )

            serializer = RecentlyViewedProductSerializer(recent_qs, many=True, context={'request': request})
            # return only the nested product dicts as a list
            product_list = [item.get('product') for item in serializer.data]
            return custom_response(
                status="success",
                status_code=status.HTTP_200_OK,
                message="Recently viewed products retrieved successfully",
                data=product_list
            )
        except Exception as e:
            return custom_response(
                status="error",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="An error occurred while retrieving recently viewed products",
                data=str(e)
            )

from rest_framework.response import Response
from rest_framework import status

class SearchByNameView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    permission_classes = [permissions.AllowAny]
    # pagination_class = CustomPagination

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        return Product.objects.filter(title__icontains=query, is_active=True).prefetch_related(
            Prefetch('images', queryset=ProductImage.objects.order_by('order'), to_attr='prefetched_images'),
            'product_tags__tag',
            'favorite_set'
        )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)

        # Build safe pagination meta when no paginator is active
        count = len(serializer.data)
        paginator = getattr(self, 'paginator', None)
        page_obj = getattr(self, 'page', None)
        if paginator is not None and page_obj is not None:
            total_pages = getattr(page_obj.paginator, 'num_pages', 1)
            current_page = getattr(page_obj, 'number', 1)
            per_page = getattr(paginator, 'page_size', count)
        else:
            total_pages = 1
            current_page = 1
            per_page = count

        # Return a standard DRF Response with the expected payload and status
        return Response(
            {
                "status": "success",
                "message": "Search results retrieved successfully",
                "meta": {
                    "count": count,
                    "total_pages": total_pages,
                    "current_page": current_page,
                    "per_page": per_page,
                },
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
    
class CategoryWiseProductsView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        category_name = self.kwargs.get('category') or self.request.query_params.get('category')
        if not category_name:
            return Product.objects.none()

        return Product.objects.filter(category__name__iexact=category_name, is_active=True).prefetch_related(
            Prefetch('images', queryset=ProductImage.objects.order_by('order'), to_attr='prefetched_images'),
            'product_tags__tag',
            'favorite_set'
        )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        
        return custom_response(
            status="success",
            status_code=status.HTTP_200_OK,
            message="Category-wise products retrieved successfully",
            data=serializer.data
        )