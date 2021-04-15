import json
from django.http.response import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from .models import *
from .mixins import WishMixin

class WishView(WishMixin,View):
    

    def get(self,request,**kwargs):
        context = super().get_context_data(request=request)
        
        return render(request,'wish/wish.html',locals())


class RemoveWishView(WishMixin):

    def post(self,request,**kwargs):
        context = super().get_context_data(request=request)
        wish = context.get('wishlist')
        print(context)
        if request.is_ajax():
            
            body = json.loads(request.body)
            slug = body.get('slug')
            wish.items.filter(product__product__slug=slug).first().delete()
            return JsonResponse({'wish_length':wish.items.count()},status=200)
            
        return HttpResponse(status=400)
