from modeltranslation.translator import TranslationOptions,register

from .models import *

@register(FAQ)
class FAQTranslation(TranslationOptions):
    fields = ['question','answer']

@register(AboutUs)
class AboutUsTranslation(TranslationOptions):
    fields = ['content']

@register(DeliveryAndPayment)
class DdeliveryAndPaymentTranslation(TranslationOptions):
    fields = ['content']

@register(TermsAndConditions)
class DdeliveryAndPaymentTranslation(TranslationOptions):
    fields = ['content']

@register(PrivacyAndPolicy)
class DdeliveryAndPaymentTranslation(TranslationOptions):
    fields = ['content']

@register(ReturnProduct)
class ReturnProductTranslation(TranslationOptions):
    fields = ['content']


@register(HowOrder)
class HowOrderTranslation(TranslationOptions):
    fields = ['content']

@register(Blog)
class BlogTranslation(TranslationOptions):
    fields = ['title','content','short_description',
            'meta_title','meta_description']