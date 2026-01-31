from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Favorite
from .serializers import FavoriteSerializer
from apps.product.serializers import ProductListSerializer
from apps.common.response import custom_response


class AddOrRemoveListFavoriteView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        favorites = Favorite.objects.filter(user=user).select_related('product').prefetch_related(
            'product__images', 
            'product__product_tags__tag',
        )
        products = [favorite.product for favorite in favorites]
        serializer = ProductListSerializer(products, many=True, context={'request': request})
        return custom_response(
            status="success",
            status_code=status.HTTP_200_OK,
            message="Favorite retrieved successfully",
            data=serializer.data
        )

    def post(self, request):
        product_id = request.data.get("product_id")
        user = request.user
        
        # Check if the user already favorited the product
        favorite = Favorite.objects.filter(user=user, product_id=product_id).first()
        if favorite:
            # If the user already favorited the product, remove the favorite
            favorite.delete()
            return custom_response(
                status="success",
                status_code=status.HTTP_200_OK,
                message="Product removed from favorites",
                data=None
            )
        
        # If the user hasn't favorited the product, create a new favorite
        Favorite.objects.create(user=user, product_id=product_id)
        return custom_response(
            status="success",
            status_code=status.HTTP_200_OK,
            message="Product added to favorites",
            data=None
        )
    
