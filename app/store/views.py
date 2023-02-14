from django.views.generic import ListView, DetailView

from cart.forms import CartAddProductForm
from .models import Category, Product


class CategoryListView(ListView):
    model = Category
    template_name = 'store/category_list.html'
    context_object_name = 'items'

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        Only not empty categories will view in html
        :param object_list:
        :param kwargs:
        :return:
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'GroceryStore'
        context['name'] = 'Categories'
        return context


class ProductListView(ListView):
    model = Product
    template_name = 'store/product_list.html'
    context_object_name = 'items'

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        'context["items"]' checking is in template 'category_list.html',
         so it's unnecessary to check it again here
        :param object_list:
        :param kwargs:
        :return:
        """
        context = super().get_context_data(**kwargs)
        context['title'] = context['items'][0].category
        context['name'] = context['items'][0].category
        return context

    def get_queryset(self):
        return Product.objects.filter(
            category__slug=self.kwargs['category_slug'])


class ProductDetail(DetailView):
    model = Product
    template_name = 'store/product.html'
    context_object_name = 'product'
    slug_url_kwarg = 'name'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.kwargs['name']
        context['cart_product_form'] = CartAddProductForm()
        return context
