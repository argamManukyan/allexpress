import json
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import View
from .models import *
from .mixin import CartMixin
from .forms import OrderForm



class CartView(CartMixin,View):
    
    def get(self,request,**kwargs):
        states = State.objects.all().order_by('id')
        cities = City.objects.filter(state=states.first())
        payment_types = PaymentTypes.objects.all()

        if request.is_ajax():
        
            try:
                cities = City.objects.filter(Q(state_id=int(request.GET['id'])))
                return JsonResponse(data=list(cities.values('name','price')),safe=False)
            except:
                return JsonResponse(data={},safe=False)

        return render(request,'cart/cart.html',locals())

    def post(self,request):
        context = super().get_context_data(request=request)
        cart = context.get('cart')
        form = OrderForm(request.POST or None)
        if form.is_valid():
            
            order = form.save()
            
            payms = request.POST.get('payments')
            
            try:
                payment_type = PaymentTypes.objects.get(id=payms)
            except:
                payment_type = None

            city_name = request.POST.get('city_name')
            try:
                city = City.objects.get(id=int(city_name))
            except:
                city = None
            order.session_key=request.session.session_key
            if request.user:
                order.user_id = request.user.id 
            order.all_total_price = cart.cart_total + (city.price if city is not None else 0)
            order.payments_id = payment_type.id if payment_type is not None else ''
            order.delivery_price = city.price if city is not None else 0
            order.save()

            cart_items = CartItem.objects.all().filter(cart=cart)

            for item in cart_items:
                ProductInOrder.objects.create(
                    order=order,
                    product=item.product,
                    product_price=int(item.product.get_prices()),
                    product_name=item.product.product.name,
                    product_image=item.product.product.productvariantimages_set.first().image,
                    qty=item.qty,                   
                    item_total_price=item.item_total
                )

                item.delete()
            cart.delete()  
            return redirect('thank-you')
        else:
            return redirect('cart')

class AddToCartView(CartMixin,View):
    
    
    def post(self,request):
        context = super().get_context_data(request=request)
        cart = context.get('cart')
        data = json.loads(request.body)
        item,created = cart.items.get_or_create(product_id=data.get('id'))
        if  created:
            item.qty = int(data.get('qty'))
            item.save()
            
        else:
            item.qty += int(data.get('qty'))
            item.save()
        

        tot_pr = 0
        for it_c in cart.items.all():
            tot_pr += it_c.item_total
        cart.cart_total = tot_pr
        cart.save()

        return JsonResponse({'cart_items':cart.items.count()},safe=False)


class RemoveFromBasket(CartMixin,View):

    def post(self,request,**kwargs):
        context = super().get_context_data(request=request)
        cart = context.get('cart')
        data = json.loads(request.body)
        item = data['item']
        
        cart.items.get(id=int(item)).delete()
        cart.save()
        cart_all_price = 0
        for item in cart.items.all():
            cart_all_price += item.item_total
        cart.cart_total = cart_all_price
        cart.save()
        return JsonResponse({'cart_total_price': cart.cart_total}, status=200)


class ChangeQtyInBasket(CartMixin,View):
    
    def post(self,request,**kwargs):
        context = super().get_context_data(request=request)
        cart = context.get('cart')
        data = json.loads(request.body)
        items, updated = CartItem.objects.update_or_create(cart=cart, id=int(data['productId']),
                                                        defaults={'qty': int(data['qty'])})
        total_price = 0
        for item in cart.items.all():
            total_price += item.item_total
        cart.cart_total = total_price
        cart.save()

        data = {'item_total_price': items.item_total,
                'cart_total_price': cart.cart_total}
        return JsonResponse(data, status=200)


class ThankYouView(View):

    def get(self,request,*args,**kwargs):
        try:
            order = Order.objects.filter(session_key=request.session.session_key).first()
        except Order.DoesNotExist:
            return redirect('home')
        if order is None:
            return redirect('home')

        return render(request,'cart/user-thank_you.html',{'order':order})    
    

        

# @csrf_exempt        
# def idramSuc(request):
    
#     link_addr = request.get_raw_uri()
#     new_text = link_addr.split('?')[1].split('&')[0].split('=')[1]
    
#     try:
#         order = Order.objects.get(id=new_text)
#         order.payments_status = 'Վճարված'
#         order.save()
        
#         if order.email != "" :
#             mail_subject = 'Պատվեր'
#             html_template = get_template('flowersmarket/email-folder/thanks-mail.html')
#             context = {
#                 # "cart": cart,
#                 'payments':order.payments,
#                 'del_type':order.delivery_type,
#                 'order': order,
#                 'products': ProductInOrder.objects.filter(order=order)

#             }
            
#             html_content = html_template.render(context)
#             from_email = settings.EMAIL_HOST_USER
#             to_list = [order.email]
#             msg = EmailMultiAlternatives(mail_subject, html_content, from_email, to_list)
#             msg.attach_alternative(html_content, "text/html")
#             msg.send()
            
#             html_template1 = get_template('flowersmarket/email-folder/Order-mail.html')
#             context = {
#                 # "cart": cart,
#                 'payments':order.payments,
#                 'del_type':order.delivery_type,
#                 'order': order,
#                 'products': ProductInOrder.objects.filter(order=order)
        
#             }
#             html_content1 = html_template1.render(context)
#             from_email_1 = settings.EMAIL_HOST_USER
#             to_list_2 = ['david.poghosyan@gios.am',settings.EMAIL_HOST_USER]
#             msg1 = EmailMultiAlternatives(mail_subject, html_content1, from_email_1, to_list_2)
#             msg1.attach_alternative(html_content1, "text/html")
#             msg1.send()
#         else:
            
#             mail_subject = 'Պատվեր'
#             html_template = get_template('flowersmarket/email-folder/thanks-mail.html')
#             context = {
#                 "cart": cart,
#                 'payments':payms,
#                 'del_type':del_type,
#                 'order': order,
#                 'products': ProductInOrder.objects.filter(order=order)

#             }
#             html_template1 = get_template('flowersmarket/email-folder/Order-mail.html')
#             context = {
#                 # "cart": cart,
#                 'payments':order.payments,
#                 'del_type':order.delivery_type,
#                 'order': order,
#                 'products': ProductInOrder.objects.filter(order=order)
        
#             }
#             html_content1 = html_template1.render(context)
#             from_email_1 = settings.EMAIL_HOST_USER
#             to_list_2 = ['david.poghosyan@gios.am',settings.EMAIL_HOST_USER]
#             msg1 = EmailMultiAlternatives(mail_subject, html_content1, from_email_1, to_list_2)
#             msg1.attach_alternative(html_content1, "text/html")
#             msg1.send()
        
      

        
#     except:
#         return redirect('home')
    

#     return render(request,'cart/idram-suc.html',locals())
    
# def idramFail(request):
    
#     link_addr = request.get_raw_uri()
#     new_text = link_addr.split('?')[1].split('&')[0].split('=')[1]
    
#     mail_subject = 'Պատվեր'
#     order = Order.objects.get(id=new_text)
#     order.payments_status = 'Չեղարկված'
#     order.status_order = 'Չեղարկված'
#     order.save()
#     html_template1 = get_template('flowersmarket/email-folder/Order-mail.html')
#     context = {
#         # "cart": cart,
#         'payments':order.payments,
#         'del_type':order.delivery_type,
#         'order': order,
#         'products': ProductInOrder.objects.filter(order=order)

#     }
#     html_content1 = html_template1.render(context)
#     from_email_1 = settings.EMAIL_HOST_USER
#     to_list_2 = ['orderflowershome@gmail.com']
#     msg1 = EmailMultiAlternatives(mail_subject, html_content1, from_email_1, to_list_2)
#     msg1.attach_alternative(html_content1, "text/html")
#     msg1.send()
   
    
#     return render(request,'cart/idram-fail.html',locals())

# def idramVchar(request,id):
    
#     idram_id = '110000350'
   
#     try:
#         s_k = request.session.session_key
#         order = Order.objects.get(id=id,session_key=s_k)
#     except:
#         return redirect('home')
    
   
    
#     return render(request,'cart/idr-red.html',locals())
    