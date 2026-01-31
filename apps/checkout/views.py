from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from apps.address.models import ShippingCharge
from apps.order.models import Order
from apps.order.serializers import OrderSerializer
from .serializers import DeliveryOptionSerializer, SelectDeliveryOptionSerializer

class ShippingChargeListViews(APIView):
    def get(self, request):
        options = ShippingCharge.objects.all()
        serializer = DeliveryOptionSerializer(options, many=True)
        return Response({"status": "success",
                        "status_code": 200,
                        "message": "Delivery options retrieved successfully",
                        "data": serializer.data})
    
class SelectShippingOptionViews(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        option_id = request.data.get("select_id")
        print("Selected Delivery Option ID:", option_id)
        try:
            option = ShippingCharge.objects.get(id=option_id)
            Order.objects.filter(user=request.user).update(shipping_charge=option.shipping_charge)
            order = Order.objects.filter(user=request.user).last()
            serializer = OrderSerializer(order, context={'request': request})
            return Response({"status": "success",
                            "status_code": 200,
                            "message": "Delivery option selected successfully",
                            "data": serializer.data})
        except ShippingCharge.DoesNotExist:
            return Response({"status": "error",
                            "status_code": 404,
                            "message": "Delivery option not found"}, status=404)