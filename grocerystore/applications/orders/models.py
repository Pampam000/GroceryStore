from django.contrib import admin
from django.db import models as m

from applications.store.models import Product
from applications.users.models import User


class Order(m.Model):
    """
    User instance could not be deleted.
    On deleting one, it's only 'User' model field 'is_active' will be changed
    to False. Look at 'users.models.User().delete()' method for more info.
    So on_delete=m.DO_NOTHING for 'users' field in this model.
    """
    user = m.ForeignKey(User, on_delete=m.DO_NOTHING, related_name='orders')
    address = m.CharField(max_length=150)
    is_paid = m.BooleanField(default=False, verbose_name='paid')
    price = m.DecimalField(default=0, max_digits=8, decimal_places=2)
    created_at = m.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)

    @admin.display(boolean=True, description="User Active",
                   ordering='user__is_active')
    def is_user_active(self) -> bool:
        return self.user.is_active

    @admin.display(description="unique products")
    def unique_products_count(self):
        return self.count_items()

    @admin.display(description="products amount")
    def total_products_amount(self):
        return sum([x.quantity for x in self.get_items()])

    def get_items(self):
        return self.items.all()

    def count_items(self):
        return self.get_items().count()


class OrderItem(m.Model):

    order = m.ForeignKey(Order, on_delete=m.CASCADE, related_name='items')
    product = m.ForeignKey(Product, on_delete=m.PROTECT,
                           related_name='order_items')
    price = m.DecimalField(max_digits=5, decimal_places=2)
    discount_price = m.DecimalField(max_digits=5, decimal_places=2)
    quantity = m.PositiveSmallIntegerField(default=1)
    total_price = m.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return str(self.pk)
