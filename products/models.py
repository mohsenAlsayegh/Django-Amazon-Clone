from django.db import models
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify


#Flaging drop down menue
FLAG_TYPES=(
    ('New', 'New')
    ('Sale', 'Sale')
    ('Feature', 'Feature')
)


#Creating products class 
class Product(models.Model):
    name = models.CharField(max_length =120)
    flag = models.CharField(max_length =10, choices = FLAG_TYPES)
    price = models.FloatField()
    images = models.ImageField(upload_to='product')
    sku = models.IntegerField()
    subtitle = models.TextField(max_length=500)
    discription = models.TextField(max_length=50000)
    tags = TaggableManager()
    brand = models.ForeignKey('Brand',related_name ='product_brand',on_delete = models.SET_NULL, null= True)
    
   

#Creating Product image calss
class ProductImages(models.Model):
    product = models.ForeignKey(Product,related_name ='product_image',on_delete=models.CASCADE)
    image = models.ImageField(upload_to ='brand')


#Creating Brand class 
class Brand(models.Model):
    name = models.CharField(max_length =100)
    image = models.ImageField(upload_to ='brand')
    slug = models.SlugField(blank = True,null = True)
    
    # overriding and saving slug name
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product,self).save(*args,**kwargs)

# Creating a review Class
class Review(models.Model):
    name = models.ForeignKey(User,related_name ='review_user',on_delete = models.SET_NULL, null=True)
    product = models.ForeignKey(Product,related_name ='review_product',on_delete = models.CASCADE)
    review = models.TextField(max_length = 500)
    rate = models.IntegerField(choices = [(i,i) for i in range(1,6)])
    created_at = models.DateTimeField(default = timezone.now)