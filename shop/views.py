from django.db.models import Q,Min,Max
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from django.http.response import JsonResponse
from django.shortcuts import render, get_object_or_404
from flatepages.models import Blog
from django.views import View
from .models import *


class HomeView(View):

    def get(self, request, *args, **kwargs):
        offers_count = len(SpecialOffer.objects.all())

        context = {}
        context['sliders'] = Sliders.objects.all()
        context['latest_products'] = Product.objects.all().order_by('-created')[:16]
        context['main_categories'] = Category.objects.filter(parent=None,view_in_homepage=True)
        context['offers_own'] = SpecialOffer.objects.all()[:2]
        context['offers_two'] = SpecialOffer.objects.all()[offers_count // 2:(offers_count // 2) + 2]
        context['sales_products'] = Product.objects.filter(Q(productvariants__sale__gt=0)).distinct()
        context['popular_products'] = Product.objects.filter(Q(is_popular=True))
        context['posts'] = Blog.objects.order_by('-id')[:3]
        return render(request, 'shop/index.html', context)


class ProductDetailView(View):

    def get(self, request, *args, **kwargs):
        context = {}
        
        context['images'] = ProductVariantImages.objects.select_related('variant', 'product') \
            .filter(product__slug=kwargs.get('slug')).all()
        context['product'] = get_object_or_404(Product, slug=kwargs['slug'])
        context['product_productvariants_set_first'] = ProductVariants.objects.filter(product_id=context['product'].id)
        context['colors'] = Color.objects.filter(productvariants__product=context['product']).distinct()
        context['sizes'] = ProductVariants.objects.filter(product_id=context['product'].id,
                                                          size__isnull=False).distinct()
        
        list_categories = [cat.id for cat in context['product'].category.get_descendants(include_self=True)]
        
        if request.GET.get('color'):
            context['product_productvariants_set_first'] = context['product_productvariants_set_first'].filter(
                color=request.GET.get('color'))
            context['images'] = context['images'].filter(variant__color=request.GET.get('color')).distinct()
            context['sizes'] = context['sizes'].filter(color=request.GET.get('color')).distinct()

        if request.GET.get('size'):
            context['product_productvariants_set_first'] = context['product_productvariants_set_first'].filter(
                size_en=request.GET.get('size'))
            context['images'] = context['images'].filter(variant__size_en=request.GET.get('size')).distinct()
            context['colors'] = context['colors'].filter(productvariants__size_en=request.GET.get('size')).distinct()

        # if not request.GET.get('color') and not request.GET.get('size') :
        context['product_productvariants_set_first'] = context['product_productvariants_set_first'].first()
        context['categories'] = context['product'].category.get_ancestors(include_self=True)
        
        
        context['latest_viewed_products'] = Product.objects.filter(slug__in=request.session['viewed_data']).exclude(id=context['product'].id)
        context['thisProductCategory'] = Product.objects.filter(category_id__in=list_categories).exclude(id=context['product'].id).exclude(id__in=context['latest_viewed_products'].values_list('id',flat=True))
       
        
        
        return render(request, 'shop/product-details.html', context)


def filter_data(request, products):
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    brand = request.GET.getlist('brand')
    sort = request.GET.getlist('sort')
    power = request.GET.getlist('power')
    volume = request.GET.getlist('volume')
    size = request.GET.getlist('size')
    color = request.GET.getlist('color')
    weight = request.GET.getlist('weight')
    ordering = request.GET.get('ordering')

    if min_price:
        products = products.filter(productvariants__filter_price__gte=min_price)
    if max_price:
        products = products.filter(productvariants__filter_price__lte=max_price)
    if brand:
        products = products.filter(brand__in=brand)
    if sort:
        products = products.filter(sort_en__in=sort)
    if power:
        products = products.filter(power_en__in=power)
    if volume:
        products = products.filter(volume_en__in=volume)
    if weight:
        products = products.filter(weight__in=weight)
    if size:
        products = products.filter(productvariants__size__in=size)
    if color:
        products = products.filter(productvariants__color_id__in=color)
    if ordering:
        products = products.order_by(ordering)
    return {'products': products.distinct()}


class CategoryDetailView(View):

    def get(self, request, *args, **kwargs):
        category = get_object_or_404(Category, slug=kwargs.get('slug'))
        list_categories = [cat.id for cat in category.get_descendants(include_self=False)]
        try:
            min_pr = Category.objects.filter(id=category.id).aggregate(Min('product__productvariants__filter_price'))['product__productvariants__filter_price__min']
            max_pr = Category.objects.filter(id=category.id).aggregate(Max('product__productvariants__filter_price'))['product__productvariants__filter_price__max']
        except:
            pass
            
        
        products = Product.objects.filter(Q(category_id=category.id) | Q(category__in=list_categories))

        # Filter
        brands = Brand.objects.prefetch_related('product_set').filter(
            Q(product__category__in=list_categories) | Q(product__category_id=category.id)).distinct()
        sorts = Product.objects.values('sort').exclude(Q(sort_en__isnull=True) | Q(sort_en=None)).distinct()
        powers = Product.objects.values('power').exclude(Q(power_en__isnull=True) | Q(power_en=None)).distinct()
        volumes = Product.objects.values('volume').exclude(Q(volume_en__isnull=True) | Q(volume_en=None)).distinct()
        
        sizes = ProductVariants.objects.filter(Q(product__category__id=category.id) | Q(product__category__in=list_categories)).values('size').exclude(
            Q(size_en__isnull=True) | Q(size_en=None)).distinct()
            
        colors = Color.objects.filter(Q(productvariants__product__category__in=list_categories) | Q(
            productvariants__product__category_id=category.id)).distinct()
        weights = Product.objects.values('weight').exclude(Q(weight_en__isnull=True) | Q(weight_en=None)).distinct()

        filter_result = filter_data(request, products).get('products')

        if request.is_ajax():
            filter_result = filter_data(request, products).get('products')
            paginator = Paginator(filter_result, 9)
            page = request.GET.get('page')
            page_product = paginator.get_page(page)
            result_dict = {}
            result_dict['products'] = render_to_string('includes/filter-data.html', context={'products': filter_result,
                                                                                             'page_product': page_product},
                                                       request=request)
            
            return JsonResponse(data=result_dict,status=200)

        paginator = Paginator(filter_result, 9)
        page = request.GET.get('page')
        page_product = paginator.get_page(page)

        return render(request, 'shop/shop.html', locals())


class AjaxSearch(View):

    def get(self, request, **kwargs):
        qs = Product.objects.filter(name__icontains=request.GET.get('q'))[:20]

        data = {}
        data['products'] = list()
        for pr in qs:
            product_dict = {}
            product_dict['name'] = pr.name
            product_dict['image'] = pr.productvariantimages_set.first().image.url
            product_dict['slug'] = pr.get_absolute_url()
            data['products'].append(product_dict)
        
        return JsonResponse(data, safe=False,)



class SalePage(View):
    
    def get(self,request,*args,**kwargs):
        
        products = Product.objects.filter(productvariants__sale__gt=0)
        filter_result = filter_data(request, products).get('products')
        
        try:
            min_pr = products.aggregate(Min('productvariants__filter_price'))['productvariants__filter_price__min']
            max_pr = products.aggregate(Max('productvariants__filter_price'))['productvariants__filter_price__max']
        except:
            pass
        
        if request.is_ajax():
            filter_result = filter_data(request, products).get('products')
            paginator = Paginator(filter_result, 9)
            page = request.GET.get('page')
            page_product = paginator.get_page(page)
            result_dict = {}
            result_dict['products'] = render_to_string('includes/filter-data.html', context={'products': filter_result,
                                                                                             'page_product': page_product},
                                                                                              request=request)
            
            return JsonResponse(data=result_dict,status=200)
            
        paginator = Paginator(filter_result, 9)
        page = request.GET.get('page')
        page_product = paginator.get_page(page)
            
        return render(request,'shop/search.html',locals())


class CatalogView(View):

    def get(self,request,**kwargs):
        categories = Category.objects.filter(parent__isnull=True)
        return render(request,'shop/catalog.html',locals())

class SearchView(View):

    def get_queryset(self):
        qs = Product.objects.filter(name__icontains=self.request.GET.get('q')).order_by('?')[:20]
        return qs

    def get(self,request,**kwargs):
        products = self.get_queryset()
        page = request.GET.get('page')
        paginator = Paginator(products,12)
        page_product = paginator.get_page(page)
        q = request.GET.get('q')
        return render(request,'shop/search.html',locals())
