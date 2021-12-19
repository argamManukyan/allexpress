import json
from django.http.response import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from .models import *
from .mixins import WishMixin
from shop.models import Product


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
            wish.items.filter(product__slug=slug).first().delete()
            return JsonResponse({'wish_length':wish.items.count()},status=200)
            
        return HttpResponse(status=400)


class ChangeWish(WishMixin):
    
    def post(self,request,**kwargs):
        context = super().get_context_data(request=request)
        wish = context.get('wishlist')

        if request.is_ajax():
            
            body = json.loads(request.body)
            id_product = body.get('id')
           
            if wish.items.filter(product_id=id_product).exists():
                
                wish.items.filter(product_id=id_product).first().delete()
                
            else:    
                try:
                    product = Product.objects.get(id=id_product)
                except:
                    return HttpResponse(status=400) 
                wish.items.create(product=product)
                wish.save()
            return HttpResponse(status=200)
            

        return HttpResponse(status=400)