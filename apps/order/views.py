from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated

from apps.order.serializers import OrderSerializer
from .models import Order
from rest_framework import generics

def order_status_distribution(request):
	status_map = {
		'pending': 'ORDER_PENDING',
		'processing': 'Processing',
		'in_shipping': 'IN_TRANSIT',
		'completed': 'Delivered',
		'cancelled': 'Cancelled',
	}
	data = []
	for status, label in status_map.items():
		count = Order.objects.filter(status=status).count()
		data.append({"status": label, "count": count})
	return JsonResponse(data, safe=False)


class OrderListView(generics.ListCreateAPIView):
	permission_classes = [IsAuthenticated]  
	queryset = Order.objects.all()
	serializer_class = OrderSerializer  # You need to define this serializer in your serializers.py file