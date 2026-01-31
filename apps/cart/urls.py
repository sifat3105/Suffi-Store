from django.urls import path
from .views import AdjustCartItemQtyView, CartRelatedProductsView, ApplyCouponView, ProceedToCheckoutView

urlpatterns = [
    path('add-to-cart/', CartRelatedProductsView.as_view(), name='add-to-cart'),
    path('get-cart-items/', CartRelatedProductsView.as_view(), name='get-cart-items'),
    path('increase-or-decrease/', AdjustCartItemQtyView.as_view(), name='adjust-cart-item-qty'),
    path('remove-from-cart/', CartRelatedProductsView.as_view(), name='remove-from-cart'),
    # path('cart/related-products/', CartRelatedProductsView.as_view(), name='cart-related-products'),
    path('apply-coupon/', ApplyCouponView.as_view(), name='apply-coupon'),
    path('set-payment-method/', ApplyCouponView.as_view(), name='set-payment-method'),

    path('proceed-to-checkout/', ProceedToCheckoutView.as_view(), name='proceed-to-checkout'),
]
