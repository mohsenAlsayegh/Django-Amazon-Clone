from rest_framework import generics

from django.contrib.auth.models import User

from .serializers import CarDetailSerializer,CartSerializer,OrderDetailSerializer,OrderSerializer
from .models import Order, OrderDetail, Cart, CartDetail,Coupon
from products.models import Product
from settings.models import DeliveryFee


class OrderListAPI(generics.ListAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

