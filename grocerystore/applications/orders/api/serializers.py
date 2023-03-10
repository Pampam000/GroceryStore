from rest_framework import serializers as s

from ..models import OrderItem

from .services.serializers import OrderMeta


class AdminOrderSerializer(s.ModelSerializer):
    class Meta(OrderMeta):
        pass


class OrderSerializer(s.ModelSerializer):
    user = s.HiddenField(default=s.CurrentUserDefault())

    class Meta(OrderMeta):
        pass


class OrderItemSerializer(s.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('pk', 'order', 'product', 'price', 'discount_price',
                  'quantity', 'total_price')
