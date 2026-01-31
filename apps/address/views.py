from rest_framework import generics, permissions, status
from .models import Address
from .serializers import AddressSerializer
from apps.common.response import custom_response

class AddressListCreateView(generics.GenericAPIView):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        addresses = Address.objects.filter(user=request.user)
        serializer = self.get_serializer(addresses, many=True)
        return custom_response(
            status="success",
            status_code=status.HTTP_200_OK,
            message="Addresses retrieved successfully",
            data=serializer.data
        )

    def post(self, request):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return custom_response(
            status="success",
            status_code=status.HTTP_201_CREATED,
            message="Address created successfully",
            data=serializer.data
        )


class AddressRetrieveUpdateDestroyView(generics.GenericAPIView):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_object(self):
        try:
            return Address.objects.get(id=self.kwargs['id'], user=self.request.user)
        except Address.DoesNotExist:
            return None

    def get(self, request, id):
        address = self.get_object()
        if not address:
            return custom_response(
                status="error",
                status_code=status.HTTP_404_NOT_FOUND,
                message="Address not found",
                data=None
            )
        serializer = self.get_serializer(address)
        return custom_response(
            status="success",
            status_code=status.HTTP_200_OK,
            message="Address retrieved successfully",
            data=serializer.data
        )

    def put(self, request, id):
        address = self.get_object()
        if not address:
            return custom_response(
                status="error",
                status_code=status.HTTP_404_NOT_FOUND,
                message="Address not found",
                data=None
            )
        serializer = self.get_serializer(address, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return custom_response(
            status="success",
            status_code=status.HTTP_200_OK,
            message="Address updated successfully",
            data=serializer.data
        )

    def delete(self, request, id):
        address = self.get_object()
        if not address:
            return custom_response(
                status="error",
                status_code=status.HTTP_404_NOT_FOUND,
                message="Address not found",
                data=None
            )
        address.delete()
        return custom_response(
            status="success",
            status_code=status.HTTP_200_OK,
            message="Address deleted successfully",
            data=None
        )


class SetDefaultAddressView(generics.GenericAPIView):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def put(self, request, id):
        try:
            address = Address.objects.get(id=id, user=request.user)
        except Address.DoesNotExist:
            return custom_response(
                status="error",
                status_code=status.HTTP_404_NOT_FOUND,
                message="Address not found",
                data=None
            )

        Address.objects.filter(user=request.user, is_default=True).exclude(id=address.id).update(is_default=False)
        address.is_default = True
        address.save()

        serializer = self.get_serializer(address)
        return custom_response(
            status="success",
            status_code=status.HTTP_200_OK,
            message="Default address set successfully",
            data=serializer.data
        )


class AvailablePostalCodesView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        """Search postal code availability.

        Query param: q (postal code string)
        Response data: {"available": "yes"} or {"available": "no"}
        """
        from .models import PostalCode

        code = request.query_params.get('q', '')
        if not code:
            return custom_response(
                status="error",
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Query parameter 'q' (postal code) is required",
                data=None,
            )

        code = code.strip()
        exists = PostalCode.objects.filter(code__iexact=code, is_available=True).exists()

        return custom_response(
            status="success",
            status_code=status.HTTP_200_OK,
            message="Postal code availability checked",
            data={"available": "yes" if exists else "no"},
        )