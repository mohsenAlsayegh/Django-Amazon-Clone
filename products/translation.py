from modeltranslation.translator import translator, TranslationOptions
from .models import Product

# for Person model
class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'flag', 'subtitle')

translator.register(Product, ProductTranslationOptions)