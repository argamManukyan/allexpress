from .models import Wish

def wish(request):
    try:
        wish_id = request.session.get('wish_id')
        wishlist = Wish.objects.get(id=wish_id)
        wish_list_items = wishlist.items.all()
    except:
        wish = Wish()
        wish.save()
        wish_list_items = wishlist.items.all()
        request.session['wish_id'] = wish.id
        wishlist = Wish.objects.get(id=wish.id)
    return locals()