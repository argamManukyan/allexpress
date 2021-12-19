from .models import Wish

def wish(request):
    try:
        wish_id = request.session.get('wish_id')
        wishlist = Wish.objects.get(id=wish_id)
        wish_list_items = wishlist.items.values_list('product_id',flat=True)
    except:
        wish = Wish()
        wish.save()
        wishlist = Wish.objects.get(id=wish.id)
        wish_list_items = wishlist.items.values_list('product_id',flat=True)
        request.session['wish_id'] = wish.id
        
    return locals()