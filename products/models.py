from django.db import models
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

#Flaging drop down menue
FLAG_TYPES=(
    ('New','New'),
    ('Sale','Sale'),
    ('Feature','Feature')
)


#Creating products class 
class Product(models.Model):
    name = models.CharField(_('name'),max_length = 120)
    flag = models.CharField(_('flag'),max_length = 10, choices = FLAG_TYPES)
    price = models.FloatField(_('price'))
    images = models.ImageField(_('image'),upload_to ='product')
    sku = models.IntegerField(_('sku'))
    subtitle = models.TextField(_('subtitle'),max_length=500)
    discription = models.TextField(_('discription'),max_length=50000)
    brand = models.ForeignKey('Brand',verbose_name = _('brand'),related_name ='product_brand',on_delete = models.SET_NULL,null= True)
    tags = TaggableManager()
    slug = models.SlugField(blank = True,null = True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product,self).save(*args, **kwargs)
   
    def __str__(self):
        return self.name

#Creating Product image calss
class ProductImages(models.Model):
    product = models.ForeignKey(Product,verbose_name = _('product'),related_name ='product_image',on_delete=models.CASCADE)
    image = models.ImageField(_('image'), upload_to ='brand')


#Creating Brand class 
class Brand(models.Model):
    name = models.CharField(_('name'),max_length =100)
    image = models.ImageField(_('image'),upload_to ='brand')
    slug = models.SlugField(blank = True,null = True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Brand, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    
# Creating a review Class
class Review(models.Model):
    name = models.ForeignKey(User,verbose_name=_('user'),related_name ='review_user',on_delete = models.SET_NULL,null=True)
    product = models.ForeignKey(Product,verbose_name = _('product'),related_name ='review_product',on_delete = models.CASCADE)
    review = models.TextField(_('review'),max_length = 500)
    rate = models.IntegerField(_('rate'),choices = [(i,i) for i in range(1,6)])
    created_at = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return f"{self.user} - {self.product} - {self.rate}" 