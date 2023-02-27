from django.db.models import QuerySet
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.views.generic.base import ContextMixin, View

from cart.services.views import CartMixin
from store.models import Product
from store.services.views import MenuMixin
from .forms import OrderCreateForm
from .models import Order


class OrderCreateView(MenuMixin, CartMixin, CreateView):
    object = None
    model = Order
    form_class = OrderCreateForm
    template_name = 'orders/create.html'
    products = None

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.products = QuerySet()

    def get_context_data(self, need_to_prepare: bool = True, **kwargs):
        context = super().get_context_data(**kwargs)
        if need_to_prepare:
            self.__prepare_for_working_with_cart()
            self.cart.check_products_amount(self.products)

        header_context = self.get_header_context(
            title='Create Order', page_title='Making Order',
            cart=self.cart.cart, error_messages=self.cart.error_messages,
            warning_messages=self.cart.warning_messages,
            total_sum=self.cart.get_total_sum(), btn_text='Place Order')

        return context | header_context

    def form_valid(self, form):
        order = form.save(commit=False)
        order.user = self.request.user
        order.save()

        self.__prepare_for_working_with_cart()

        if self.cart.create_order_items(order, self.products):
            return redirect('orders:success', order)
        else:
            order.delete()
            return self.render_to_response(self.get_context_data(
                need_to_prepare=False))

    def __prepare_for_working_with_cart(self):
        self.products = Product.objects.filter(slug__in=self.cart.cart)
        slugs = [x.slug for x in self.products]
        self.cart.sort(slugs)


class SuccessMakingOrder(MenuMixin, ContextMixin, View):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        header_context = self.get_header_context(
            title='Success', page_title='Order has been made successfully')
        return context | header_context

    def get(self, request, **kwargs):
        data = self.get_context_data(**kwargs)
        return render(request, 'orders/created.html', data)
