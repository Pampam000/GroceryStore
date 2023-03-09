from rest_framework.serializers import ModelSerializer

from applications.orders.models import Order, OrderItem


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ('users', 'address', 'is_paid', 'price', 'created_at')


class OrderItemSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('order', 'product', 'price', 'discount_price', 'quantity',
                  'total_price')
