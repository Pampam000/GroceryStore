from django.shortcuts import render, redirect

from cart.views import CartView
from .forms import OrderCreateForm
from .models import OrderItem, Order
from .services.views import CartChecker


class OrderCreateView(CartView):
    object = None
    model = Order
    form_class = OrderCreateForm
    template_name = 'orders/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        result = CartChecker(self.cart).check_cart_items_in_db()

        context['title'] = 'Create Order'
        context['cart'] = result.cart
        context['messages'] = result.messages

        return context

    def form_valid(self, form):
        order = form.save(commit=False)
        order.user = self.request.user
        order.save()

        for item in self.cart:
            OrderItem.objects.create(order=order, product=item['product'],
                                     quantity=item['quantity'])
            item['product'].amount -= item['quantity']
            item['product'].save()

        self.cart.clear()

        return redirect('orders:success', order)


def success(request, order):
    return render(request, 'orders/created.html',
                  {'order': order})