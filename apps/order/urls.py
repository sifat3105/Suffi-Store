from django.urls import path
from .views import order_status_distribution, OrderListView

urlpatterns = [
    path('status-distribution/', order_status_distribution, name='order-status-distribution'),

    path('order-list/', OrderListView.as_view(), name='order-list'),
]
