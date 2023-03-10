from django.db.models import F
from rest_framework import status, mixins
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from applications.cart.services.views import CartView
from applications.store.models import Product
from .serializers import OrderItemSerializer, OrderSerializer, \
    AdminOrderSerializer
from ..models import OrderItem, Order


class AdminOrderViewSet(mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.ListModelMixin,
                        GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = AdminOrderSerializer
    permission_classes = (IsAdminUser,)


class OrderViewSet(CartView,
                   mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    products = None

    def list(self, request, *args, **kwargs):
        self.__prepare_for_working_with_cart()
        self.cart.check_products_amount(self.products)
        response = self.__create_response()
        return Response(response, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):

        if self.cart.cart:

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            order = serializer.save()

            self.__prepare_for_working_with_cart()

            if self.cart.create_order_items(order, self.products):

                order.price = F('price') + self.cart.get_total_sum()
                order.save(update_fields=['price'])
                order.refresh_from_db()
                serializer.save(price=str(order.price))
                self.cart.clear()
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            else:
                order.delete()
                response = self.__create_response()
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {'detail': "Impossible to create the order. Cart is empty."},
                status=status.HTTP_406_NOT_ACCEPTABLE)

    def __prepare_for_working_with_cart(self):
        self.products = Product.objects.filter(slug__in=self.cart.cart)
        slugs = [x.slug for x in self.products]
        self.cart.sort(slugs)

    def __create_response(self) -> dict:
        return {
            "errors": self.cart.error_messages,
            "warnings": self.cart.warning_messages,
            "cart": self.cart.cart,
            "total_sum": self.cart.get_total_sum()
        }


class OrderItemViewSet(ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    http_method_names = ('get', 'delete')
    permission_classes = (IsAdminUser,)
