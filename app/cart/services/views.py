from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import redirect
from django.views import View

from ..cart import Cart


class CartMixin(LoginRequiredMixin, View):
    cart = None

    def handle_no_permission(self):
        return redirect('log-in')

    def setup(self, request: WSGIRequest, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.cart = Cart(self.request.session)
