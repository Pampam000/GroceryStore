from django.views.generic import ListView, DetailView

from cart.forms import CartAddProductForm
from .models import Category, Product
from .services.views import MenuMixin


class CategoryListView(MenuMixin, ListView):
    model = Category
    template_name = 'store/category_list.html'
    context_object_name = 'items'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        header_context = self.get_header_context(title='GroceryStore',
                                                 name='Categories')
        return context | header_context

    def get_queryset(self):
        """
        Only not empty categories will view in html
        """
        return Category.objects.filter(product__isnull=False).distinct()


class ProductListView(MenuMixin, ListView):
    model = Product
    template_name = 'store/product_list.html'
    context_object_name = 'items'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.kwargs)

        title = self.kwargs['category_slug']
        header_context = self.get_header_context(title=title, name=title)
        return context | header_context

    def get_queryset(self):
        return Product.objects.filter(
            category__slug=self.kwargs['category_slug']). \
            select_related('category', 'producer')


class ProductDetail(MenuMixin, DetailView):
    model = Product
    template_name = 'store/product.html'
    context_object_name = 'product'
    slug_url_kwarg = 'name'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        header_context = self.get_header_context(
            title=self.kwargs['name'], cart_product_form=CartAddProductForm())
        return context | header_context

    def get_queryset(self):
        return Product.objects.filter(
            slug=self.kwargs['name']).select_related('producer')
