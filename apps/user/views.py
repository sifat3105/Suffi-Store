from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import AccountSerializer
from .models import Account
from apps.common.response import custom_response
from apps.address.models import Address
from apps.address.serializers import AddressSerializer
from apps.order.models import Order
from apps.order.serializers import OrderSerializer



class MyAccountView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        account = Account.objects.get(user=request.user)
        personal_info = AccountSerializer(account).data
        addresses = AddressSerializer(Address.objects.filter(user=request.user), many=True, context={'request': request}).data
        orders = OrderSerializer(Order.objects.filter(user=request.user).prefetch_related('items__product'), many=True).data
        return custom_response(
            status="success",
            status_code=status.HTTP_200_OK,
            message="Account retrieved successfully",
            data={
                "personal_info": personal_info,
                "addresses": addresses,
                "orders": orders
            }
        )
    
class MyProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        account = Account.objects.get(user=request.user)
        personal_info = AccountSerializer(account).data
        return custom_response(
            status="success",
            status_code=status.HTTP_200_OK,
            message="Account retrieved successfully",
            data=personal_info
        )
    
    def put(self, request):
        account = Account.objects.get(user=request.user)
        serializer = AccountSerializer(account, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return custom_response(
                status="success",
                status_code=status.HTTP_200_OK,
                message="Account updated successfully",
                data=serializer.data
            )
        return custom_response(
            status="error",
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Account update failed",
            data=serializer.errors
        )
    

class AddressListView(generics.ListCreateAPIView):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def get(self, request):
        addresses = AddressSerializer(self.get_queryset(), many=True, context={'request': request}).data
        return custom_response(
            status="success",
            status_code=status.HTTP_200_OK,
            message="Addresses retrieved successfully",
            data=addresses
        )

    def post(self, request):
        serializer = AddressSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return custom_response(
                status="success",
                status_code=status.HTTP_201_CREATED,
                message="Address created successfully",
                data=serializer.data
            )
        return custom_response(
            status="error",
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Address creation failed",
            data=serializer.errors
        )
    
class MyOrdersView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items__product')

    def get(self, request):
        orders = OrderSerializer(self.get_queryset(), many=True).data
        return custom_response(
            status="success",
            status_code=status.HTTP_200_OK,
            message="Orders retrieved successfully",
            data=orders
        )   



