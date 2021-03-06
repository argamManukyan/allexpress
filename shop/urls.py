from django.urls import path

from .views import *

urlpatterns = [
    path('index/',HomeView.as_view(),name='home'),
    path('product/<slug>/',ProductDetailView.as_view(),name='product-details'),
    path('category/<slug>/',CategoryDetailView.as_view(),name='category-details'),
    path('catalog/',CatalogView.as_view(),name='catalog'),
    path('sales/',SalePage.as_view(),name='sales'),
    path('search/',SearchView.as_view(),name='search')
]
