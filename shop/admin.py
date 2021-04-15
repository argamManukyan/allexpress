from django.contrib import admin
from django.contrib.admin.decorators import register
from django.utils.html import format_html
from mptt.admin import DraggableMPTTAdmin
from modeltranslation.admin import TabbedDjangoJqueryTranslationAdmin, TranslationStackedInline
from .models import *
from .forms import ImageUploadForm


class ProductVariantTabularInline(TranslationStackedInline):
    model = ProductVariants
    extra = 0
    form = ImageUploadForm


class ProductImageTabularInline(admin.TabularInline):
    model = ProductVariantImages
    extra = 0


@register(Sliders)
class SliderAdmin(TabbedDjangoJqueryTranslationAdmin):

    def image_tag(self, obj):
        return format_html(f'<img src="{obj.image.url}" style="width:150px;height:150px;margin-right:10px" /> ')

    image_tag.short_description = 'Image'

    list_display = ['id', 'image_tag']


class CategoryAdmin(DraggableMPTTAdmin, TabbedDjangoJqueryTranslationAdmin):
    pass


admin.site.register(Category, CategoryAdmin)


@admin.register(Brand)
class BrandAdmin(TabbedDjangoJqueryTranslationAdmin):
    pass


@admin.register(Color)
class ColorAdmin(TabbedDjangoJqueryTranslationAdmin):
    pass


@admin.register(Product)
class ProductAdmin(TabbedDjangoJqueryTranslationAdmin):
    inlines = [ProductVariantTabularInline, ProductImageTabularInline]

    def save_model(self, request, obj, form, change):
        obj.save()
        for i in request.FILES:
            idx = i.split('-image')[0] + '-id'
            if len(request.POST.get(idx)) != 0:
    
                for img in request.FILES.getlist(i):
                    ProductVariantImages.objects.create(product_id=obj.id, variant_id=request.POST.get(idx), image=img)



@admin.register(SpecialOffer)
class SpecialOfferAdmin(TabbedDjangoJqueryTranslationAdmin):
    pass


admin.site.register(ProductVariantImages)
