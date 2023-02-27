from django.shortcuts import render, redirect

from app import settings
from store.services.views import MenuMixin
from .cart import Cart
from .forms import CartAddProductForm
from .services.views import CartMixin


class CartAddItemView(CartMixin):

    @staticmethod
    def post(request):
        form = CartAddProductForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            product = data['product']
            quantity = data['quantity']
            cart = Cart(request.session)
            cart.add(product, quantity)

            return redirect(data['from_url'])


class CartDetailView(MenuMixin, CartMixin):

    def handle_no_permission(self):
        return redirect('log-in')

    def get_context_data(self):
        if not self.request.session.get(settings.CART_SESSION_ID):
            self.request.session[settings.CART_SESSION_ID] = {}
        cart = Cart(self.request.session)
        header_context = self.get_header_context(
            title="Cart", page_title="Your cart", cart=cart.cart,
            total_sum=cart.get_total_sum())
        return header_context

    def get(self, request):
        return render(request, 'cart/detail.html', self.get_context_data())


class CartRemoveItemView(CartMixin):
    @staticmethod
    def get(request, **kwargs):
        cart = Cart(request.session)
        cart.remove(kwargs['product_slug'])
        return redirect(request.META["HTTP_REFERER"])
