from django.shortcuts import render, redirect

from django.views.generic import ListView,DetailView

from .models import Product,Brand,Review,ProductImages
from django.db.models import Q , F, Value
from django.db.models.aggregates import Count,Sum,Avg,Max,Min
from django.views.decorators.cache import cache_page


@cache_page(60 * 1)
def mydebug(request):
    # data = Product.objects.all()
    
    # column number -------
    # data = Product.objects.filter(price = 20)
    # data = Product.objects.filter(price__gt = 98)
    # data = Product.objects.filter(price__gte = 98)
    # data = Product.objects.filter(price__lt = 25)
    # data = Product.objects.filter(price__range = (80,83))
    
    # relation -------
    # data = Product.objects.filter(brand__id = 5)
    # data = Product.objects.filter(brand__id__gt = 200)
    
    # text -------
    # data = Product.objects.filter(name__contains = 'Bob')
    # data = Product.objects.filter(name__startswith = 'Bob')
    # data = Product.objects.filter(name__endswith = 'Thomas')
    # data = Product.objects.filter(price__isnull = True)
    
    # dates -------
    # data = Product.objects.filter(date_colum__year = '2022')
    # data = Product.objects.filter(date_colum__month = '2022')
    # data = Product.objects.filter(date_colum__day = '2022')
    
    # complex queries -------
    # data = Product.objects.filter(flag = 'New' , price__gt = 98)
    # data = Product.objects.filter(flag = 'New').filter(price__gt = 98)
    # data = Product.objects.filter(
    #     Q(flag = 'New') &
    #     Q(price__gt = 98)
    #     )
    
    # data = Product.objects.filter(
    #     Q(flag = 'New') |
    #     Q(price__gt = 98)
    #     )
    
    # data = Product.objects.filter(
    #     ~ Q(flag = 'New') |
    #     Q(price__gt = 98)
    #     )

    #Field Reference -------
    # data = Product.objects.filter(quantity= F('price'))
    # data = Product.objects.filter(quantity= F('category__id'))
    
    #Order -------
    # data = Product.objects.all().order_by('name') # ACS
    # data = Product.objects.order_by('name')
    # data = Product.objects.order_by('-name')  # DES
    # data = Product.objects.order_by('-name', 'price') # DES and ACS ny price
    # data = Product.objects.filter(price__gt=80).order_by('name')
    # data = Product.objects.order_by('name')[:10]
    # data = Product.objects.earliest('name')
    # data = Product.objects.latest('name')
    
    # limit fields -------
    # data = Product.objects.values('name','price')
    # data = Product.objects.values_list('name','price')
    # data = Product.objects.only('name','price')
    # data = Product.objects.defer('discription','subtitle')
    
    # select related ------------
    # data = Product.objects.select_related('brand').all()  # Forign key, one-to-one ---> merge the two tables then fetch
    # data = Product.objects.prefetch_related('brand').all() # many-to-many
    # data = Product.objects.select_related('brand').select_related('category').all()
    
    # aggregation ------ (Count,min,max,sum,avg) should be used with {comment in template}
    # data = Product.objects.aggregate(
    #     myavg = Avg('price'),
    #     mycount  = Count('id')
    #     ) 
     
    # Annotation-------
    # data = Product.objects.annotate(is_new= Value(0))
    # data = Product.objects.annotate(price_with_tax= F('price')*1.15)
    
    data = Product.objects.all()
    
    return render(request, "products/debug.html", {"data":data})


# query set : [products] : filter -----> related data 
# context :  user #other type of data ---> unrelated type of data 

class  ProductList(ListView):
    model =  Product
    paginate_by = 50
    
    
 # context{}, query set : Product.object.all():1 : option 2: method :override
 # query set : main query  : detail
 # context : extra data    : reviews, images 
class  ProductDetail(DetailView): 
    model =  Product 
    
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs) # dict : object one prouduct
        context["reviews"] = Review.objects.filter(product=self.get_object()) # make filter and give review for one product
        context['images']= ProductImages.objects.filter(product=self.get_object()) # make filter and give imge for one product
        context['related']=Product.objects.filter(brand=self.get_object().brand) # make filter and give brand
        return context
    

class BrandList(ListView):
    model = Brand
    paginate_by = 50
    queryset = Brand.objects.annotate(product_count = Count('product_brand'))
    
    
class BrandDetail(ListView):
    model = Product
    template_name = 'products/brand_detail.html'
    paginate_by = 50
    
    def get_queryset(self):
        brand = Brand.objects.get(slug=self.kwargs['slug']) #kwargs select all the parametrs
        queryset = super().get_queryset().filter(brand=brand)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["brand"] = Brand.objects.filter(slug=self.kwargs['slug']).annotate(product_count = Count('product_brand'))[0]
        return context
    

def add_reveiw(request,slug):
    product = Product.objects.get(slug=slug)
    
    review = request.POST['review']
    rate = request.POST['rating']   #request.POST['rating']  if template method is GET request.GET['rating'] or GET request.POST.get['rating']  from list to function
    # add review
    
    Review.objects.create(
        user = request.user,
        product = product,
        review = review,
        rate = rate
    )
    return redirect(f'/products/{slug}')
    
    # return product_detail