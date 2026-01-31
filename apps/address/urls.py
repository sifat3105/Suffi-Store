from django.urls import path
from .views import AddressListCreateView, AddressRetrieveUpdateDestroyView, SetDefaultAddressView, AvailablePostalCodesView


urlpatterns = [
    path('add-address/', AddressListCreateView.as_view(), name='address-list-create'),
    path('address-list/', AddressListCreateView.as_view(), name='address-list-create'),
    path('update-address/<int:id>/', AddressRetrieveUpdateDestroyView.as_view(), name='address-detail'),
    path('address/<int:id>/set-default/', SetDefaultAddressView.as_view(), name='address-set-default'),
    path('availability-postal-codes/', AvailablePostalCodesView.as_view(), name='availability-postal-codes'),
]
