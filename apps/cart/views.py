from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from apps.product.models import Product
from .models import Cart, CartItem, CouponCode
from .serializers import CartSerializer
from apps.common.response import custom_response
from apps.cart.utils import CartUtils
from django.db import transaction
from decimal import Decimal
from apps.order.models import Order
from apps.order.models import Order, OrderItem
from django.db import transaction
from apps.order.serializers import OrderSerializer
import logging

logger = logging.getLogger(__name__)
    
    
class CartRelatedProductsView(APIView, CartUtils):
    permission_classes = [IsAuthenticated]

    serializer_class = CartSerializer

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart = Cart.objects.prefetch_related("items__product").get(user=request.user)
        
        list = self.serializer_class(cart).data['items']
        metadata = self.serializer_class(cart).data
        return Response({
            "status": "success",
            "status_code": status.HTTP_200_OK,
            "message": "Cart retrieved successfully",
            "data": self.serializer_class(cart).data
        })
    
    def post(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        try:
            product_id = request.data.get("product_id")
            product_quantity = request.data.get("quantity")

            product = Product.objects.get(id=product_id)
            if product_quantity > product.quantity:
                return Response({
                    "status": "error",
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": "Requested quantity exceeds available stock"
                })
            
            # product.quantity -= product_quantity
            # product.save()

            try:
                cart_item = cart.items.get(product=product)
                cart_item.quantity += product_quantity
                cart_item.save()
            except CartItem.DoesNotExist:
                    cart_item = CartItem.objects.create(
                        cart=cart,
                        product_id=product.id,
                        quantity=product_quantity
                    )
            return custom_response(
                status="success",
                status_code=status.HTTP_200_OK,
                message="Cart updated successfully",
                data=CartSerializer(cart).data
            )
        except Exception as e:
            return custom_response(
                status="error",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message=f"An error occurred: {e}"
            )
        
    def delete(self, request):
        try:
            item_id = request.data.get("item_id")
            list_of_item_ids = request.data.get("list_of_item_ids", [])

            if item_id and not list_of_item_ids:
                list_of_item_ids = [item_id]

            if isinstance(list_of_item_ids, int):
                list_of_item_ids = [list_of_item_ids]

            if isinstance(list_of_item_ids, str):
                list_of_item_ids = [p.strip() for p in list_of_item_ids.split(",") if p.strip()]

            try:
                ids = [int(i) for i in list_of_item_ids]
            except Exception:
                return custom_response(
                    status="error",
                    status_code=status.HTTP_400_BAD_REQUEST,
                    message="item_id/list_of_item_ids must be an integer, a list of integers or a comma-separated string of integers"
                )

            qs = CartItem.objects.filter(id__in=ids, cart__user=request.user)

            matched_ids = list(qs.values_list('id', flat=True))
            missing_ids = [i for i in ids if i not in matched_ids]
            cart = Cart.objects.filter(user=request.user).first()
            if not matched_ids:
                return custom_response(
                    status="error",
                    status_code=status.HTTP_404_NOT_FOUND,
                    message="No matching products found in your cart",
                    data= self.serializer_class(cart).data
                )

            

            with transaction.atomic():
                deleted_count, _ = qs.delete()
                if cart:
                    try:
                        cart.calculate_total()
                    except Exception:
                        logger.exception("Failed to recalculate cart total after deleting items")

            return custom_response(
                status="success",
                status_code=status.HTTP_200_OK,
                message="Products removed from cart successfully",
                data = self.serializer_class(cart).data
            )

        except Exception as e:
            logger.exception("Error deleting cart items")
            return custom_response(
                status="error",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message=f"An error occurred: {e}"
            )


class AdjustCartItemQtyView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        product_id = request.data.get("product_id")
        action = request.data.get("action")
        print(product_id, action)

        product = Product.objects.filter(id=product_id).first()
        if not product:
            return Response({
                "status": "error",
                "status_code": status.HTTP_404_NOT_FOUND,
                "message": "Product not found in store"
            })
        try:
            cart = Cart.objects.get(user=request.user)
            cart_item = cart.items.get(product__id=product_id)
        except Cart.DoesNotExist:
            return Response({
                "status": "error",
                "status_code": status.HTTP_404_NOT_FOUND,
                "message": "Cart not found"
            })
        except CartItem.DoesNotExist:
            return Response({
                "status": "error",
                "status_code": status.HTTP_404_NOT_FOUND,
                "message": "Product not found in cart"
            })

        if action == "increase":
            if product.quantity <= 0:
                return Response({
                    "status": "error",
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": "Insufficient stock to increase quantity"
                })
            else:
                # product.quantity -= 1
                # product.save()
                cart_item.quantity += 1
                cart_item.save()
                return Response({
                    "status": "success",
                    "status_code": status.HTTP_200_OK,
                    "message": "Product quantity increased successfully",
                    "data": CartSerializer(cart).data
                })
        elif action == "decrease":
            if cart_item.quantity <= 1:
                return Response({
                    "status": "error",
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": "Product quantity cannot be less than 1"
                })
            else:
                # product.quantity += 1
                # product.save()
                cart_item.quantity -= 1
                cart_item.save()
                return Response({
                    "status": "success",
                    "status_code": status.HTTP_200_OK,
                    "message": "Product quantity decreased successfully",
                    "data": CartSerializer(cart).data
                })
        return Response({
            "status": "error",
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": "Invalid action. Use 'increase' or 'decrease'."
        })

        
class ApplyCouponView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        coupon_code = request.data.get("coupon_code")
        user = request.user
        if not coupon_code:
            return custom_response(
                status="error",
                status_code=status.HTTP_400_BAD_REQUEST,
                message="coupon_code is required"
            )

        is_valid = CouponCode.objects.filter(code=coupon_code, active=True).exists()
        if not is_valid:
            return custom_response(
                status="error",
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Invalid or inactive coupon code"
            )
        
        # Get the CouponCode object first
        coupon_obj = CouponCode.objects.get(code=coupon_code, active=True)
        # Cart.objects.filter(user=user).update(coupon_code=coupon_obj, is_coupon_applied=True)
        cart, _ = Cart.objects.get_or_create(user=user)
        try:
            discount_percentage = coupon_obj.discount_percentage
            cart_discount = (cart.calculated_sub_total * discount_percentage) / Decimal('100')
            cart.discount = cart_discount
            # cart.total_price = cart.calculated_sub_total - cart_discount
            cart.save()
        except Exception as e:
            logger.exception("Error applying coupon to cart")
            return custom_response(
                status="error",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message=f"An error occurred while applying the coupon: {e}"
            )
        return custom_response(
            status="success",
            status_code=status.HTTP_200_OK,
            message="Coupon applied successfully",
            data=CartSerializer(cart).data
        )

from django.utils import timezone
class ProceedToCheckoutView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def post(self, request):
        cart = Cart.objects.filter(user=request.user).first()
        if not cart or not cart.items.exists():
            return custom_response(
                status="error",
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Your cart is empty. Add items to proceed to checkout."
            )


        try:
            with transaction.atomic():
                # Create the order
                order = Order.objects.create(
                    user=request.user,
                    order_id=f"ORD-{request.user.id}-{cart.id}-{timezone.now().strftime('%Y%m%d%H%M%S')}",
                    tracking_id=f"TRK-{request.user.id}-{cart.id}-{timezone.now().strftime('%Y%m%d%H%M%S')}",
                    sub_total=cart.calculated_sub_total,
                    total_price=cart.total_price,
                    shipping_charge=cart.shipping_charge_amount,
                    vat_amount=cart.calculated_vat,
                    discount=cart.discount,
                    status='PENDING'
                )

                # Get all product names in a list
                cart_items_name = [item.product.title for item in cart.items.all()]
                # Store all product names in the order's products_name field (as comma-separated string)
                order.products_name = ', '.join(cart_items_name)
                order.save()

                # Create order items with the correct product name for each item
                for cart_item in cart.items.all():
                    OrderItem.objects.create(
                        order=order,
                        product=cart_item.product,
                        quantity=cart_item.quantity,
                        product_price=cart_item.product.price
                    )

                # Optionally, clear the cart after checkout
                cart.items.all().delete()
                cart.discount = 0
                cart.save()

            return Response({
                "status": "success",
                "status_code": status.HTTP_200_OK,
                "message": "Proceed to checkout successful",
                "data": self.serializer_class(order).data
            }
            )
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.exception("Error during checkout")
            return custom_response(
                status="error",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message=f"An error occurred during checkout: {e}"
            )
