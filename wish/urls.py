from wish.views import WishView,RemoveWishView
from django.urls import path
from django.views.decorators import csrf
urlpatterns = [
    path('wish/',WishView.as_view(),name='wish'),
    # path('add-wish/',WishView.as_view(),name='add-wish'),
    path('remove-wish/',csrf.csrf_exempt(RemoveWishView.as_view()),name='remove-wish'),
    # path('add-wish/',WishView.as_view(),name='add-wish'),
]