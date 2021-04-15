from shop.models import Category

def return_categories(request):
    categories_menu = Category.objects.all()
    all_categories = Category.objects.all()
    return {'categories_menu':categories_menu,'categories':all_categories}