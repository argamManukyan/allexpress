from .models import Cart, CartItem


def get_cart(request):
    try:
        cart_id = request.session.get('cart_id')
        cart = Cart.objects.get(id=cart_id)
        cart_items = len(cart.items.all())
    except:
        cart = Cart()
        cart.save()
        request.session['cart_id'] = cart.id
        cart = Cart.objects.get(id=request.session['cart_id'])
        cart_items = len(cart.items.all())

    return {'cart': cart, 'cart_items': cart_items}
