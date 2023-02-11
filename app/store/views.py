from django.views.generic import ListView, DetailView

from .models import Category, Product


class CategoryListView(ListView):
    model = Category
    template_name = 'store/products_and_categories.html'
    context_object_name = 'items'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'GroceryStore'
        context['name'] = 'Categories'
        return context


class ProductListView(ListView):
    model = Product
    template_name = 'store/products_and_categories.html'
    context_object_name = 'items'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if context['items']:
            title = context['items'][0].category
        else:
            title = Category.objects.get(slug=self.kwargs['category_slug'])
        context['title'] = title
        context['name'] = title
        return context

    def get_queryset(self):
        return Product.objects.filter(category__slug=
                                      self.kwargs['category_slug'])


class ProductDetail(DetailView):
    model = Product
    template_name = 'store/product.html'
    context_object_name = 'product'
    slug_url_kwarg = 'name'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.kwargs['name']
        return context
