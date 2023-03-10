from applications.orders.models import Order


class OrderMeta:
    model = Order
    fields = ('pk', 'user', 'address', 'is_paid', 'price', 'created_at')
    read_only_fields = ('is_paid', 'price')
