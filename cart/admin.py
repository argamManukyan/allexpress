from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin,ImportExportActionModelAdmin
from import_export.resources import ModelResource
from import_export.widgets import ForeignKeyWidget
from import_export import fields

class PaymentIconsTabularInline(admin.TabularInline):
    model = PaymentTypeIcons
    extra = 1


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