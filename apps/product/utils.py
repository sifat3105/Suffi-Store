from django.db.models import Prefetch, Sum
from apps.product.models import Product, WeeklySpecialProduct, ProductImage, Tag
import random, datetime


def get_best_selling_products(limit=9):
    base_qs = Product.objects.filter(
        is_active=True,
        stock_status__in=['in-stock', 'low-stock']
    ).annotate(
        total_sold=Sum('orderitem__quantity')
    )

    prefetch_images = Prefetch(
        'images',
        queryset=ProductImage.objects.order_by('order', 'id'),
        to_attr='prefetched_images'
    )

    qs_prefetch = base_qs.prefetch_related(
        prefetch_images,
        'product_tags__tag',
        'favorite_set'
    )

    best_selling_qs = qs_prefetch.filter(total_sold__gt=0).order_by('-total_sold')
    best_selling_products = list(best_selling_qs[:limit])

    if len(best_selling_products) >= limit:
        return best_selling_products

    best_sellers_list = list(best_selling_products)
    best_sellers_count = len(best_sellers_list)

    if best_sellers_count > 0:
        remaining_needed = limit - best_sellers_count
        best_seller_ids = [p.id for p in best_sellers_list]

        random_products = list(
            qs_prefetch.exclude(id__in=best_seller_ids).order_by('?')[:remaining_needed]
        )

        return best_sellers_list + random_products
    else:
        return list(qs_prefetch.order_by('?')[:limit])
    



def get_weekly_special_products():
    weekly_specials = WeeklySpecialProduct.objects.filter(
        start_date__lte=datetime.date.today(),
        end_date__gte=datetime.date.today()
    ).order_by('order')

    product_ids = [ws.product_id for ws in weekly_specials]

    if not product_ids:
        return []

    prefetch_images = Prefetch(
        'images',
        queryset=ProductImage.objects.order_by('order', 'id'),
        to_attr='prefetched_images'
    )

    products_qs = Product.objects.filter(id__in=product_ids).prefetch_related(
        prefetch_images,
        'product_tags__tag',
        'favorite_set'
    )

    from django.db.models import Case, When
    ordering = Case(*[When(id=pid, then=pos) for pos, pid in enumerate(product_ids)])
    products = list(products_qs.order_by(ordering))

    return products


def get_recently_viewed_products(request):

        if 'recently_viewed' not in request.session:
            return []
        
        recently_viewed = request.session['recently_viewed']
        
        product_ids = [item['id'] for item in recently_viewed]
        products = Product.objects.filter(id__in=product_ids).prefetch_related(
            'images', 
            'product_tags__tag',
            'favorite_set'
        )
        return products

