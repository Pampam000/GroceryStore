from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect

from store.services.views import MenuMixin
from .cart import Cart
from .forms import CartAddProductForm
from .services.views import LoginRequiredCartView


class CartAddItemView(LoginRequiredCartView):

    @staticmethod
    def post(request: WSGIRequest):
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            product = data['product']
            quantity = data['quantity']
            cart = Cart(request.session)
            cart.add(product, quantity)

            return redirect(data['from_url'])


class CartDetailView(MenuMixin, LoginRequiredCartView):

    def get_context_data(self):
        total_sum = self.cart.get_total_sum()
        table_headers = self.cart.get_th_for_table()
        header_context = self.get_header_context(
            title="Cart", page_title="Your cart", cart=self.cart.cart,
            total_sum=total_sum, table_headers=table_headers)
        return header_context

    def get(self, request: WSGIRequest):
        return render(request, 'cart/detail.html', self.get_context_data())


class CartRemoveItemView(LoginRequiredCartView):

    @staticmethod
    def get(request: WSGIRequest, **kwargs):
        cart = Cart(request.session)
        cart.remove(kwargs['product_slug'])
        return redirect(request.META["HTTP_REFERER"])
