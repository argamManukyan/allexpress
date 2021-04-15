from django.urls import path
from .views import *

urlpatterns = [

    path('faq/',FAQView.as_view(),name='faq'),
    path('about-us/',AboutUsView.as_view(),name='about-us'),
    path('how-to-order/',how_order,name='how-to-order'),
    path('privacy-policy/',PrivacypolicyView.as_view(),name='privacy-policy'),
    path('return-product/',return_process,name='return_proces'),
    path('delivery-and-payment/',DeliveryAdnPaymentView.as_view(),name='delivery-and-payment'),
    path('blog/',BlogListView.as_view(),name='blog'),
    path('blog/<slug>/',BlogDetailView.as_view(),name='blog-details'),
]
