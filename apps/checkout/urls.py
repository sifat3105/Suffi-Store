from django.urls import path
from .views import ShippingChargeListViews, SelectShippingOptionViews


urlpatterns = [
    path('delivery-charge-list/',ShippingChargeListViews.as_view(), name='delivery-options'),
    path('select-delivery-option/',SelectShippingOptionViews.as_view(), name='select-delivery-option'),
]