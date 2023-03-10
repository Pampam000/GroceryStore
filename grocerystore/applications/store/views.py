from django.views.generic import ListView, DetailView

from applications.cart.forms import CartAddProductForm
from .models import Category, Product
from grocerystore.views import MenuMixin


class CategoryListView(MenuMixin, ListView):
    model = Category
    template_name = 'store/list.html'
    context_object_name = 'items'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        header_context = self.get_header_context(title='GroceryStore',
                                                 page_title='Categories')
        return context | header_context

    def get_queryset(self):
        """
        Only not empty categories will view in html
        """
        return Category.objects.filter(product__isnull=False).distinct()


class ProductListView(MenuMixin, ListView):
    model = Product
    template_name = 'store/list.html'
    context_object_name = 'items'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        title = context['items'][0].category.name
        header_context = self.get_header_context(title=title, page_title=title)
        return context | header_context

    def get_queryset(self):
        return list(Product.objects.filter(
            category__slug=self.kwargs['category_slug']).
                    select_related('category', 'producer'))


class ProductDetail(MenuMixin, DetailView):
    model = Product
    template_name = 'store/product.html'
    context_object_name = 'product'
    slug_url_kwarg = 'name'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = context['object']
        header_context = self.get_header_context(
            title=title, form=CartAddProductForm(), page_title=title)
        return context | header_context

    def get_queryset(self):
        return Product.objects.filter(
            slug=self.kwargs['name']).select_related('producer')
