from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import OrderItem


@receiver(post_save, sender=OrderItem)
def post_save_order_item(**kwargs):

    order_item = kwargs['instance']
    product = order_item.product

    product.amount = F('amount') - order_item.quantity
    product.save(update_fields=['amount'])
