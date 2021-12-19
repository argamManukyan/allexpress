from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin,ImportExportActionModelAdmin
from import_export.resources import ModelResource
from import_export.widgets import ForeignKeyWidget
from import_export import fields

class PaymentIconsTabularInline(admin.TabularInline):
    model = PaymentTypeIcons
    extra = 1


class OrderItemsInline(admin.TabularInline):

    model = ProductInOrder
    extra = 1
    readonly_fields = ['product','product_price','item_total_price','product_name','product_image','qty']


class OrderAdmin(admin.ModelAdmin):

    list_display = [field.name for field in Order._meta.fields]
    inlines = [OrderItemsInline]

admin.site.register(Order,OrderAdmin)
admin.site.register(Cart)
admin.site.register(CartItem)


class PaymentAdmin(admin.ModelAdmin):

    inlines = [PaymentIconsTabularInline]

admin.site.register(PaymentTypes,PaymentAdmin)

class StateResource(ModelResource):
    
    state = fields.Field(attribute='state',column_name='state',widget=ForeignKeyWidget(State,'name'))

    class Meta:
        model = City


class ExcellModelImport(ImportExportModelAdmin):
    resource_class = StateResource

admin.site.register(State,ImportExportModelAdmin)
admin.site.register(City,ExcellModelImport)