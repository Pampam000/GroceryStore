import json

from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.views import ModelWithProtectedRelationViewSet
from .permissions import IsAdminOrReadOnly
from .serializers import ProductSerializer, CategorySerializer, \
    ProducerSerializer, ProductBatchSerializer
from ..models import Product, Category, Producer, ProductBatch
from applications.cart.services.views import CartView


class ProductViewSet(CartView, ModelWithProtectedRelationViewSet):
    queryset = Product.objects.select_related()
    serializer_class = ProductSerializer
    permission_classes = (IsAdminOrReadOnly,)

    @action(detail=True, url_path='add-to-cart',
            permission_classes=(IsAuthenticated,))
    def add_to_cart(self, request, pk):
        product = json.loads(self.get_object().as_cart_item())
        quantity = request.data['quantity'] if request.data.get('quantity') \
            else 1
        self.cart.add(product, quantity)
        return Response(self.cart.cart)

    @action(detail=True, url_path='remove-from-cart',
            permission_classes=(IsAuthenticated,))
    def remove_from_cart(self, request, pk):
        product = self.get_object()
        slug = product.slug
        self.cart.remove(slug)
        return Response(self.cart.cart)


class CategoryViewSet(ModelWithProtectedRelationViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)

    def get_queryset(self):
        if self.request.user.is_staff:
            return super().get_queryset()
        else:
            return self.queryset.filter(product__isnull=False).distinct()

    @action(detail=True, serializer_class=ProductSerializer)
    def products(self, request, pk):
        queryset = Product.objects.filter(category__pk=pk)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ProducerViewSet(ModelWithProtectedRelationViewSet):
    queryset = Producer.objects.all()
    serializer_class = ProducerSerializer
    permission_classes = (IsAdminUser,)


class ProductBatchViewSet(ModelViewSet):
    queryset = ProductBatch.objects.all()
    serializer_class = ProductBatchSerializer
    permission_classes = (IsAdminUser,)
