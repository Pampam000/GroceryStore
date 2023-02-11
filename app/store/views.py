from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render

from .models import Category, Product


def index(request):
    categories = Category.objects.all()
    return render(request, 'store/products_and_categories.html',
                  {'title': 'Categories', 'items': categories})


def show_products_in_category(request: WSGIRequest, name):
    category = Category.objects.get(slug=name)
    # products = Product.objects.filter(category=1)
    products = category.category_products.all()

    return render(request, 'store/products_and_categories.html',
                  {'title': name, 'items': products})


def show_product_info(request, name):
    product = Product.objects.get(slug=name)
    return render(request, 'store/product.html',
                  {'title': name, 'product': product})
