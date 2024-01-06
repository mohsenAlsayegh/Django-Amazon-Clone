from rest_framework import serializers
from taggit.serializers import TagListSerializerField,TaggitSerializer
from .models import Product, Brand, Review , ProductImages


class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
       model = ProductImages
       fields = ['images']
       
class ProductReviwesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['product','rate', 'created_at']
        
class ProductListSerializer(TaggitSerializer,serializers.ModelSerializer):
    brand = serializers.StringRelatedField()
    tags = TagListSerializerField()

    class Meta:
        model = Product
        fields = ['name','price','flag','images','subtitle','sku','discription','brand','review_count','avg_rate','tags']
       


class ProductDetailSerializer(TaggitSerializer,serializers.ModelSerializer):
    brand = serializers.StringRelatedField()
    image = ProductImagesSerializer(source= 'product_image',many=True)
    reviews =ProductReviwesSerializer(source='review_product',many=True)
    tags = TagListSerializerField()
    
    class Meta:
        model = Product
        fields = ['name','price','flag','images','subtitle','sku','discription','brand','review_count','avg_rate','image','reviews','tags']
        

        
class BrandListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'
        

class BrandDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'