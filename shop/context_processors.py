from shop.models import Category

def return_categories(request):
    categories_menu = Category.objects.all()
    all_categories = Category.objects.all()
    
    request.session['viewed_data'] = []
    
    if 'product' in  request.get_full_path() :
        if request.resolver_match.kwargs.get('slug') not in request.session['viewed_data']:
            request.session['viewed_data'].append(request.resolver_match.kwargs.get('slug')) 
    
    return {'categories_menu':categories_menu,'categories':all_categories}