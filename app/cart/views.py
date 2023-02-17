from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import CreateView

from store.models import Product
from .cart import Cart
from .forms import CartAddProductForm


class CartView(LoginRequiredMixin, CreateView):

    def handle_no_permission(self):
        return redirect('log-in')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cart = None

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.cart = Cart(self.request.session)


class CartAddItemView(CartView):
    form_class = CartAddProductForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        product = Product.objects.get(slug=kwargs['product_slug'])

        if form.is_valid():
            self.cart.add(
                product=product, quantity=form.cleaned_data['quantity'])

        return redirect('store:product', product.slug)


class CartDetailView(CartView):
    def get(self, request, *args, **kwargs):
        return render(request, 'cart/detail.html',
                      {'title': 'Cart', 'cart': self.cart})


class CartRemoveItemView(CartView):
    def get(self, request, *args, **kwargs):
        product = Product.objects.get(slug=kwargs['product_slug'])
        self.cart.remove(product)
        return redirect('cart_detail')
