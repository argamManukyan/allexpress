from django.views import View
from .models import Wish

class WishMixin(View):

    def get_context_data(self,**kwargs):
        request = kwargs.get('request')
      
        try:
            wish_id = request.session.get('wish_id')
            wishlist = Wish.objects.get(id=wish_id)
            wish_list_items = wishlist.items.all()
        except:
            wish = Wish()
            wish.save()
            wishlist = Wish.objects.get(id=wish.id)
            wish_list_items = wishlist.items.all()
            request.session['wish_id'] = wish.id
            
        return {
            'wishlist':wishlist
        }