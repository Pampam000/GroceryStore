import json

import django
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from cart.cart import Cart
from .serializers import ProductSerializer, CategorySerializer, \
    ProducerSerializer, ProductBatchSerializer
from ..models import Product, Category, Producer, ProductBatch


class DestroyProtectedField(ModelViewSet):
    class Meta:
        abstract = True

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except django.db.models.deletion.ProtectedError as e:
            return Response(data={'detail': str(e)},
                            status=status.HTTP_409_CONFLICT)


class ProductViewSet(DestroyProtectedField):
    queryset = Product.objects.select_related()
    serializer_class = ProductSerializer

    @action(detail=True, url_path='add-to-cart')
    def add_to_cart(self, request, pk):
        cart = Cart(request.session)
        product = json.loads(self.get_object().as_cart_item())
        quantity = request.data['quantity'] if request.data.get('quantity') \
            else 1
        cart.add(product, quantity)
        return Response(cart.cart)

    @action(detail=True, url_path='remove-from-cart')
    def remove_from_cart(self, request, pk):
        cart = Cart(request.session)
        product = self.get_object()
        slug = product.slug
        cart.remove(slug)
        return Response(cart.cart)


class CategoryViewSet(DestroyProtectedField):
    queryset = Category.objects.all()  # filter(product__isnull=False).distinct()
    serializer_class = CategorySerializer

    @action(detail=True, serializer_class=ProductSerializer)
    def products(self, request, pk):
        queryset = Product.objects.filter(category__pk=pk)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ProducerViewSet(DestroyProtectedField):
    queryset = Producer.objects.all()
    serializer_class = ProducerSerializer


class ProductBatchViewSet(ModelViewSet):
    queryset = ProductBatch.objects.all()
    serializer_class = ProductBatchSerializer
