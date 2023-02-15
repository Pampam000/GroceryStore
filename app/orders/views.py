from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import CreateView

from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart


class OrderCreateView(LoginRequiredMixin, CreateView):

    form_class = OrderCreateForm
    template_name = 'orders/create.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cart = None

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.cart = Cart(self.request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        return context

    def form_valid(self, form):

        order = form.save(commit=False)
        order.user = self.request.user
        order.save()

        for item in self.cart:
            OrderItem.objects.create(order=order,
                                     product=item['product'],
                                     quantity=item['quantity'])
        self.cart.clear()

        return redirect('orders:success', order)


def success(request, order):
    return render(request, 'orders/created.html',
                  {'order': order})
