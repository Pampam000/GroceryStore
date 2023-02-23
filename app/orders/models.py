from django.db import models as m

from user.models import User
from store.models import Product


class Order(m.Model):
    user = m.ForeignKey(User, on_delete=m.CASCADE, related_name='orders')
    address = m.CharField(max_length=150)
    is_paid = m.BooleanField(default=False)

    def __str__(self):
        return str(self.pk)

    @property
    def get_total_cost(self):
        return sum(item.get_cost for item in self.items)


class OrderItem(m.Model):
    order = m.ForeignKey(Order, on_delete=m.CASCADE, related_name='items')
    product = m.ForeignKey(Product, on_delete=m.SET_NULL, null=True)
    quantity = m.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return str(self.pk)

    @property
    def get_cost(self):
        return round(self.get_product_total_price * self.quantity, 2)

    @property
    def get_product_total_price(self):
        return self.product.total_price()





