from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import CreateView

from ..cart import Cart


class CartView(LoginRequiredMixin, CreateView):

    def handle_no_permission(self):
        return redirect('log-in')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cart = None

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.cart = Cart(self.request.session)
