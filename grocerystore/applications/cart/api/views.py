from django.core.handlers.wsgi import WSGIRequest
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from ..services.views import CartView


class CartViewSet(CartView, ViewSet):
    http_method_names = ('get',)
    permission_classes = (IsAuthenticated,)

    def list(self, request: WSGIRequest):
        return Response(self.cart.cart, status=status.HTTP_200_OK)
