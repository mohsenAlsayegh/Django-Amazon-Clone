from django.shortcuts import render
from django.views.generic import ListView,DetailView
from .models import Product,Brand,Review,ProductImages

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
    
    
    
class BrandDetail(ListView):
    model = Product
    template_name = 'products/brand_detail.html'
    
    def get_queryset(self):
        brand = Brand.objects.get(slug=self.kwargs['slug']) #kwargs select all the parametrs
        queryset = super().get_queryset().filter(brand=brand)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["brand"] = Brand.objects.get(slug=self.kwargs['slug'])
        return context
    

    
    