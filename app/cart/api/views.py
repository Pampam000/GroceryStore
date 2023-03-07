from django.core.handlers.wsgi import WSGIRequest
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from ..cart import Cart


class CartViewSet(ViewSet):
    http_method_names = ('get',)
    permission_classes = (IsAuthenticated,)

    def list(self, request: WSGIRequest):
        cart = Cart(request.session)
        result = cart.cart
        return Response(result, status=status.HTTP_200_OK)
