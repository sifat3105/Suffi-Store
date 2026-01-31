from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from apps.product.utils import get_recently_viewed_products
from apps.product.serializers import ProductListSerializer

class CustomPagination(PageNumberPagination):
    page_size = 10                   
    page_size_query_param = "per_page"   
    max_page_size = 100
    
    def get_paginated_response(self, data):
        return Response({
            "status": "success",
            "status_code": 200,
            "message": "Paginated data retrieved successfully",
            "data": {
                "count": self.page.paginator.count,
                "total_pages": self.page.paginator.num_pages,
                "current_page": self.page.number,
                "per_page": self.get_page_size(self.request),
                "results": data,
                
            }
        })
    
    def _rerecently_viewed_products(self):
        return ProductListSerializer(get_recently_viewed_products(self.request), many=True).data
