from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import *

urlpatterns = [
    path('cart/',CartView.as_view(),name='cart'),
    path('add-to-cart/',csrf_exempt(AddToCartView.as_view()),name='add-to-cart'),
    path('remove_from_basket/',csrf_exempt(RemoveFromBasket.as_view()),name='remove_from_basket'),
    path('change-qty/',csrf_exempt(ChangeQtyInBasket.as_view()),name='change-qty'),
    path('order-more/',ThankYouView.as_view(),name='thank-you')

]
