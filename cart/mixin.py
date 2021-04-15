from .models import Cart
from django.views.generic import View

class CartMixin(View):

    

    def get_context_data(self,**kwargs):
        request = kwargs.get('request')
        try:
            cart_id = request.session.get('cart_id')
            cart = Cart.objects.get(id=cart_id)
            cart_items = len(cart.items.all())
        except:
            cart = Cart()
            cart.save()
            request.session['cart_id'] = cart.id
            cart = Cart.objects.get(id=cart.id)
            cart_items = len(cart.items.all())

        return {
            'cart':cart,
            'cart_items':cart_items
        }