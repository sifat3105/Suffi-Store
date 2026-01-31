from django.contrib.auth import get_user_model
from django.db.models import Count, Sum, Q
from apps.product.models import Product
from django.utils import timezone
from django.db import models
import json
from decimal import Decimal
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from django.db.models import Count, Sum, Q, F
from django.db.models.functions import Coalesce
from apps.review.models import Review
from apps.cart.models import Cart
from apps.user.models import User


def dashboard_callback(request, context):
    """
    Dashboard callback for admin dashboard.
    Aggregates data from all apps for visualization with cards, charts, and graphs.
    """
    today = timezone.now().date()
    thirty_days_ago = today - timedelta(days=30)

    # User stats (minimal fields available on custom User)
    login_users = User.objects.count()
    staff_users = User.objects.filter(is_staff=True).count()
    guest_users = 0

    # Product stats
    total_products = Product.objects.count()
    active_products = Product.objects.filter(is_active=True).count()
    featured_products = 0

    # Parts stats
    total_parts = 0
    active_parts = 0

    # Order stats
    total_orders = 0
    # revenue_total = OrderHistory.objects.exclude(status='CANCELLED').aggregate(total=Sum('total_price'))['total'] or Decimal('0.00')
    # avg_order_value = (revenue_total / total_orders) if total_orders else Decimal('0.00')
    recent_orders = list(
        []
    )
    orders_by_status = list(
        []
    )

    # Cart stats
    total_carts = Cart.objects.count()

    # Review stats
    total_reviews = Review.objects.count()

    # Shipping / payment config stats
    shipping_methods = 0
    active_stripe_configs = 0

    # delivered_orders = OrderHistory.objects.filter(status__iexact='delivered')
    total_amount_of_sell = 0    
    total_number_of_sell = 0


    # ==================== USER STATISTICS ====================
    total_users = User.objects.count()
    verified_users = User.objects.filter(is_active=True).count()
    staff_users = User.objects.filter(is_staff=True).count()
    new_users_30d = User.objects.filter(last_login__gte=thirty_days_ago).count()
    
    # User growth trend (last 12 months including current) - using proper calendar months
    user_growth = []
    current_date = today.replace(day=1)  # Start from first day of current month
    
    for i in range(12):
        # Calculate month boundaries
        month_start = current_date - relativedelta(months=11 - i)
        month_end = month_start + relativedelta(months=1)
        
        count = User.objects.filter(
            last_login__gte=month_start,
            last_login__lt=month_end
        ).count()
        
        user_growth.append({
            'month': month_start.strftime('%b %Y'),
            'count': count
        })

    # Reviews per month (last 12 months including current) - using proper calendar months
    review_growth = []
    current_date = today.replace(day=1)  # Start from first day of current month
    
    for i in range(12):
        # Calculate month boundaries
        month_start = current_date - relativedelta(months=11 - i)
        month_end = month_start + relativedelta(months=1)
        
        # Count reviews for this calendar month
        rcount = Review.objects.filter(
            created_at__date__gte=month_start,
            created_at__date__lt=month_end
        ).count()
        
        review_growth.append({
            'month': month_start.strftime('%b %Y'),
            'count': rcount
        })

    status_charts = []
    

    
        
    # Update context with lightweight, project-relevant data
    context.update({
        # User Statistics
        'total_users': total_users,
        'verified_users': verified_users,
        'staff_users': staff_users,
        'new_users_30d': new_users_30d,
        'user_growth': json.dumps(list(user_growth)),
        'review_growth': json.dumps(list(review_growth)),
        'total_users': login_users+guest_users,
        'login_users': login_users,
        'staff_users': staff_users,
        'guest_users': guest_users,
        'total_products': total_products,
        'active_products': active_products,
        'featured_products': featured_products,
        'total_parts': total_parts,
        'active_parts': active_parts,
        'total_orders': total_orders,
        'total_revenue': float(total_amount_of_sell),
        'total_sell': total_number_of_sell,
        'recent_orders': recent_orders,
        'orders_by_status': orders_by_status,
        'total_carts': total_carts,
        'total_reviews': total_reviews,
        'shipping_methods': shipping_methods,
        'active_stripe_configs': active_stripe_configs,
        'last_30d_orders': 0,
    })

    return context