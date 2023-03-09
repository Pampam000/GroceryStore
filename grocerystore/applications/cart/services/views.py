from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import redirect
from django.views import View

from ..cart import Cart


class CartView(View):
    cart = None

    def dispatch(self, request: WSGIRequest, *args, **kwargs):
        self.cart = Cart(request.session)
        return super().dispatch(request, *args, **kwargs)


class LoginRequiredCartView(LoginRequiredMixin, CartView):
    def handle_no_permission(self):
        return redirect('log-in')
