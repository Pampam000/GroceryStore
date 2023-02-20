from django.shortcuts import render, redirect

from store.models import Product
from store.services.views import MenuMixin
from .forms import CartAddProductForm
from .services.views import CartView


class CartAddItemView(CartView):
    form_class = CartAddProductForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        product = Product.objects.get(slug=kwargs['product_slug'])

        if form.is_valid():
            self.cart.add(
                product=product, quantity=form.cleaned_data['quantity'])

        return redirect('store:product', product.slug)


class CartDetailView(MenuMixin, CartView):

    def get(self, request, *args, **kwargs):
        return render(request, 'cart/detail.html',
                      self.get_header_context(title='Cart', cart=self.cart))


class CartRemoveItemView(CartView):
    def get(self, request, *args, **kwargs):
        product = Product.objects.get(slug=kwargs['product_slug'])
        self.cart.remove(product)
        return redirect('cart_detail')
