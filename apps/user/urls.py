from django.urls import path
from .views import (
    MyAccountView,
    MyProfileView,
    AddressListView,
    MyOrdersView,
)

urlpatterns = [
    # Account overview (personal info, addresses, and orders)
    path('my-account/', MyAccountView.as_view(), name='my-account'),

    # Profile info (view and update)
    path('my-profile/', MyProfileView.as_view(), name='my-profile'),
    # path('my-profile/update/', MyProfileView.as_view(), name='my-profile-update'),

    # User addresses (list + create)
    # path('address/', AddressListView.as_view(), name='address-list'),

    # User orders (list all)
    path('my-orders', MyOrdersView.as_view(), name='my-orders'),
]
