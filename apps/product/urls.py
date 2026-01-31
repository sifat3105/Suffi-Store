from django.urls import path
from .views import ProductListView, ProductDetailView, HomePageDataView,  WeeklySpecialProductView, BestSellingProductView, RecentlyViewedProductView , SearchByNameView,CategoryWiseProductsView, ProductFiltersView

urlpatterns = [
    path('home-page-data/', HomePageDataView.as_view(), name='home-page-data'),
    path('best-selling-products/', BestSellingProductView.as_view(), name='best-selling-products'),
    path('weekly-special-products/', WeeklySpecialProductView.as_view(), name='weekly-special-products'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/filters/', ProductFiltersView.as_view(), name='product-filters'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('recently-viewed-products/', RecentlyViewedProductView.as_view(), name='recently-viewed-products'),
    # path('recently-viewed-reviews/', RecendtReviewsView.as_view(), name='recently-viewed-reviews'),

    path('search-by-name/', SearchByNameView.as_view(), name='search-by-name'),
    path('category-wise-products/<str:category>/', CategoryWiseProductsView.as_view(), name='category-wise-products'),
]