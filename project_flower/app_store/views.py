from django.shortcuts import render

from .models import *


# Create your views here.


def index(request):
    categories = Category.objects.filter(parent=None)

    subcategories_titles = []

    for category in categories:
        for subcategory_1 in category.subcategories.all():
            for subcategory_2 in subcategory_1.subcategories.all():
                if subcategory_2.title not in subcategories_titles:
                    subcategories_titles.append(subcategory_2.title)

    products = Product.objects.all()
    context = {
        'categories': categories,
        'subcategories_titles': subcategories_titles,
        'products': products
    }

    return render(request, 'app_store/index.html', context)
