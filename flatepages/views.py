from django.shortcuts import render
from django.views.generic import DetailView,ListView,View
from .models import *


class BlogListView(ListView):

    template_name = 'flatepages/blog.html'
    queryset = Blog.objects.all().order_by('-id')
    context_object_name = 'posts'

    

class BlogDetailView(DetailView):
    queryset = Blog.objects.all()
    template_name = 'flatepages/blog-details.html'
    context_object_name = 'blog'

    def get(self, request,*args, **kwargs):
        
        obj = self.get_object()      
        if not kwargs['slug'] in request.session:
            obj.views_count += 1
            obj.save(force_update=True)
            request.session[kwargs['slug']] = kwargs['slug']

        context = {}
        context['blog'] = obj
        return render(request,self.template_name,context)


class FAQView(ListView):

    queryset = FAQ.objects.all()
    template_name = 'flatepages/faq.html'
    context_object_name = 'questions'


class AboutUsView(View):

    def get(self, request, *args, **kwargs):
        about = AboutUs.objects.first()
        return render(request,'flatepages/about-us.html',locals())

class DeliveryAdnPaymentView(View):

    def get(self,request,**kwargs):
        delivery_payment = DeliveryAndPayment.objects.first()
        return  render(request,'flatepages/delivery-payment.html',locals())


class PrivacypolicyView(View):
    
    def get(self,request,**kwargs):
        policy = PrivacyAndPolicy.objects.first()
        return  render(request,'flatepages/delivery-payment.html',locals())



def how_order(request):
    how_order = HowOrder.objects.first()
    return render(request,'flatepages/how-order.html',locals())


def return_process(request):
    return_process = ReturnProduct.objects.first()
    return render(request,'flatepages/return-product.html',locals())


def error404(request, exception, template_name='errors/error404.html'):
    return render(request, 'flatepages/404.html',status=404)