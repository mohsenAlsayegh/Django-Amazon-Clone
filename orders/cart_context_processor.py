from .models import Cart,CartDetail

# get or create 

def get_cart_data(request):
    
    if request.user.is_authenticated:
        cart , created = Cart.objects.get_or_create(user=request.user, status = 'Inprogress')
        cart_detail = CartDetail.objects.filter(order = cart)
        return{'cart_data': cart , 'cart_detail':cart_detail}
    
    else:
        return{}