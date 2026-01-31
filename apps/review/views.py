# removed incorrect Response import (requests.Response) — DRF views shouldn't use this here
from rest_framework.views import APIView
from rest_framework import status, generics, permissions
from apps.product.models import Product
from apps.order.models import OrderItem
from apps.common.response import custom_response
from .serializers import ContactUsSerializer, ReviewSerializer
from .models import Review

from django.db.models import Count

class ReviewsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, product_id):
        try:
            user = request.user
            product = Product.objects.get(id=product_id)

            order_count = OrderItem.objects.filter(
                order__user=user,
                product=product
            ).values("order").distinct().count()

            if order_count == 0:
                return custom_response(
                    status="error",
                    status_code=status.HTTP_400_BAD_REQUEST,
                    message="You have not placed an order for this product yet"
                )

            # `Review` uses `reviewer` FK to User, not `user`
            review_count = Review.objects.filter(product=product, reviewer=user).count()

            if review_count >= order_count:
                return custom_response(
                    status="error",
                    status_code=status.HTTP_400_BAD_REQUEST,
                    message="You have already reviewed this product for all your orders"
                )

            # create Review: set `reviewer` to the User instance
            review = Review.objects.create(
                product=product,
                reviewer=user,
                rating=request.data.get("rating"),
                comment=request.data.get("comment"),
            )

            return custom_response(
                status="success",
                status_code=status.HTTP_201_CREATED,
                message="Review created successfully",
                data=ReviewSerializer(review).data,
            )

        except Product.DoesNotExist:
            return custom_response(
                status="error",
                status_code=status.HTTP_404_NOT_FOUND,
                message="Product not found"
            )
        except Exception as e:
            return custom_response(
                status="error",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message=f"An error occurred: {e}"
            )
        
# class ViewAllReviews(generics.ListAPIView):
#     permission_classes = [permissions.AllowAny]
#     serializer_class = ReviewSerializer
#     queryset = Review.objects.filter(is_approved=True)
#     def get_queryset(self):
#         return self.queryset.order_by('-rating', '-id')

class ViewAllReviews(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        try:
            review = Review.objects.filter(is_approved=True).order_by('-rating')[:5]
            serializer = ReviewSerializer(review, many=True)
            return custom_response(
                status="success",
                status_code=status.HTTP_200_OK,
                message="Recently viewed products retrieved successfully",
                data=serializer.data
            )
        except Exception as e:
            return custom_response(
                status="error",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="An error occurred while retrieving recently viewed products",
                data=str(e)
            )

class ContactUsView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ContactUsSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            contact_us = serializer.save()
            return custom_response(
                status="success",
                status_code=status.HTTP_201_CREATED,
                message="Your message has been received. We will get back to you shortly.",
                data=ContactUsSerializer(contact_us).data
            )
        return custom_response(
            status="error",
            status_code=status.HTTP_400_BAD_REQUEST,
            message="There was an error with your submission.",
            data=serializer.errors
        )
            