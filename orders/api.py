from rest_framework import generics
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
import datetime
from rest_framework import status


from .serializers import CarDetailSerializer,CartSerializer,OrderDetailSerializer,OrderSerializer
from .models import Order, OrderDetail, Cart, CartDetail,Coupon
from products.models import Product
from settings.models import DeliveryFee
from accounts.models import Address


class OrderListAPI(generics.ListAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get_queryset(self):
        queryset = super(OrderListAPI, self).get_queryset()
        user =User.objects.get(username=self.kwargs['username'])
        queryset = queryset.filter(user=user)
        return queryset

    # def list(self,request, *args, **kwargs):
    #     queryset = super(OrderListAPI, self).get_queryset()
    #     user =User.objects.get(username=self.kwargs['username'])
    #     queryset = queryset.filter(user=user)
    #     data = OrderSerializer(queryset, many=True).data
    #     return Response({'orders':data})
    

class OrderDetailAPI(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    
class ApplyCouponAPI(generics.GenericAPIView):
    
    def post(self,request,*args,**kwargs):
        user =User.objects.get(username=self.kwargs['username']) #url
        coupon = get_object_or_404(Coupon, code=request.data['coupon_code']) #request body
        cart = Cart.objects.get(user=user,status='Inprogress')
        deliver_fee = DeliveryFee.objects.last().fee
        
        
        if coupon and coupon.quantity > 0:
            today_date = datetime.datetime.today().date()
            if today_date >= coupon.start_date and coupon.end_date:
                coupon_value = round(cart.cart_total/100*coupon.discount,2)
                sub_total = cart.cart_total - coupon_value
                total = sub_total + coupon_value
                
                cart.coupon = coupon
                cart.total_with_coupon = sub_total
                cart.save()
                
                coupon.quantity -= 1
                coupon.save()
                return Response({'message' :'coupon has applied successfully'})
            else:
                return Response({'message' :'coupon is invalid or expired'})
            
        return Response({'message':'coupon not found'},status=status.HTTP_200_OK)

class CreateOrderAPI(generics.GenericAPIView):
    def post(self,request,*args,**kwargs):
        user =User.objects.get(username=self.kwargs['username'])
        code = request.data['payment_code']
        address = request.data['address_id']
        
        cart = Cart.objects.get(user=user,status='Inprogress')
        cart_detail = CartDetail.objects.filter(order = cart )
        user_address = Address.objects.get(id=address)
        
        # cart :order | cart_detail :order
        new_order = Order.objects.create(
            user = user,
            status = 'Received',
            code = code,
            address = user_address,
            coupon = cart.coupon,
            total_with_coupon = cart.total_with_coupon,
            total = cart.cart_total
            )
        
        # order detail
        for item in cart_detail:
            product = Product.objects.get(id=item.product.id)
            OrderDetail.objects.create(
                order = new_order,
                producut = product,
                quantity = item.qauntity,
                price = product.price,
                total = round(item.qauntity*product.price,2)
                )
            
            # decrease product quantity
            product.quantity -= item.qauntity
            product.save()
            
        # close the acrt
        cart.status = 'Completed'
        product.save()

        # send email
        return Response({'message':'order was created successfully'},status=status.HTTP_201_CREATED)
class CartCreatUpdateDelete(generics.GenericAPIView):
    pass
    