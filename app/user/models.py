from django.contrib import admin
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    def delete(self, using=None, keep_parents=False):
        self.is_active = False
        self.save(update_fields=['is_active'])

    @admin.display(description="last 5 orders")
    def get_orders(self):
        result = list(self.orders.all().order_by('-pk')[:5])
        return result if result else None

    def orders_amount(self):
        return self.orders.all().count()
