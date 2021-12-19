from django.contrib import admin
from django.urls import path,include
from django.conf.urls import handler404
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static,settings
from shop.views import AjaxSearch
from django.conf.urls import include, re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/',include('ckeditor_uploader.urls')),
    re_path(r'^rosetta/', include('rosetta.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('result/',AjaxSearch.as_view(),name='result'),
    path('',include('wish.urls')),
    
]

urlpatterns += i18n_patterns(
    path('i18n/', include('django.conf.urls.i18n')),
    path('',include('flatepages.urls')),
    path('',include('accounts.urls')),
    path('',include('shop.urls')),
    path('',include('cart.urls')),
    
    prefix_default_language=False,
)



if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


handler404 = 'flatepages.views.error404'
