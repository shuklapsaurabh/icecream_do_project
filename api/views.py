from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from api.models import Order, Flavor
from api.serializers import OrderSerializer, FlavorSerializer
# from .tasks import process_payment
from api.tasks import process_payment
from django.db.models import Sum
from rest_framework.decorators import api_view, permission_classes
from .serializers import FlavorSerializer
from .models import Flavor
from rest_framework import status

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        order = serializer.save(user=request.user)
        process_payment.delay(order.id)
        return Response({'status': 'Order placed', 'order_id': order.id})
    return Response(serializer.errors, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_flavor(request):
    serializer = FlavorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_stats(request):
    data = Order.objects.values('flavor__name').annotate(total_qty_ordered=Sum('quantity'))
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_flavors(request):
    flavors = Flavor.objects.all()
    serializer = FlavorSerializer(flavors, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_orders(request):
    orders = Order.objects.filter(user=request.user)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)
