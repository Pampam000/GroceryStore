from django.db.models import F
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from cart.cart import Cart
from store.models import Product
from .serializers import OrderItemSerializer, OrderSerializer
from ..models import OrderItem, Order


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        cart = Cart(request.session)
        if cart.cart:

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            order = serializer.save()

            products = Product.objects.filter(slug__in=cart.cart)
            slugs = [x.slug for x in products]
            cart.sort(slugs)

            if cart.create_order_items(order, products):

                order.price = F('price') + cart.get_total_sum()
                order.save(update_fields=['price'])
                order.refresh_from_db()
                serializer.save(price=str(order.price))
                cart.clear()
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            else:
                order.delete()
                return Response(
                    {'error': cart.error_messages,
                     'detail': cart.warning_messages},
                    status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': "Cart is empty"},
                            status=status.HTTP_406_NOT_ACCEPTABLE)


class OrderItemViewSet(ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    http_method_names = ('get', 'delete')
