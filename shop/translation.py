from modeltranslation.translator import TranslationOptions,register
from .models import *

@register(Category)
class CategoryTranslation(TranslationOptions):
    fields = ['name','meta_title','meta_description']

@register(Brand)
class BrandTranslation(TranslationOptions):
    fields = ['name',]

@register(Color)
class ColorTranslation(TranslationOptions):
    fields = ['name',]

@register(Product)
class ProductTranslation(TranslationOptions):
    fields = ['name','manufactured',
    'country','volume','weight','power',
    'sort','qty_in_coll'
    ]

@register(ProductVariants)
class ProductVariantsTranslation(TranslationOptions):
    fields = ['size']

@register(SpecialOffer)
class SpecialOfferTranslation(TranslationOptions):
    fields = ['name','description']
    
@register(Sliders)
class SlidersTranslation(TranslationOptions):
    fields = ['context']