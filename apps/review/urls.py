from django.urls import path
from .views import ReviewsView,ContactUsView,ViewAllReviews

urlpatterns = [
    path('create-reviews/<int:product_id>/', ReviewsView.as_view(), name='reviews'),
    path('view-all-reviews/', ViewAllReviews.as_view(), name='reviews'),
    path('contact-us/', ContactUsView.as_view(), name='contact-us'),
]