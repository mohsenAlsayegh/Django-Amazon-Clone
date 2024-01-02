from rest_framework import serializers
from .models import Product, Brand, Review , ProductImages




class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
       model = ProductImages
       fields = ['images']
       
class ProductReviwesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['product','rate', 'created_at']
        
class ProductListSerializer(serializers.ModelSerializer):
    brand = serializers.StringRelatedField()
    review_count = serializers.SerializerMethodField()
    avg_rate = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = '__all__'
       
        
    def get_review_count(self,object):
        reviews = object.review_count()
        return reviews

    def get_avg_rate(self,object):
        avg = object.avg_rate()
        return avg

class ProductDetailSerializer(serializers.ModelSerializer):
    brand = serializers.StringRelatedField()
    review_count = serializers.SerializerMethodField()
    avg_rate = serializers.SerializerMethodField()
    image = ProductImagesSerializer(source= 'product_image',many=True)
    reviews =ProductReviwesSerializer(source='review_product',many=True)
    class Meta:
        model = Product
        fields = '__all__'
        
    def get_review_count(self,object):
        reviews = object.review_product.all().count()
        return reviews
    
    def get_avg_rate(self,object):
        total = 0
        reviews = object.review_product.all()
        
        if len(reviews) > 0:
            for item in reviews:
                total += item.rate
                
            avg = total/len(reviews)
        else :
            avg = 0
        return avg
        
class BrandListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'
        

class BrandDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'