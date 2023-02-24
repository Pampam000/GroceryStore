from django.db.models import F
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from .models import ProductBatch, Product, Category


@receiver(post_save, sender=ProductBatch)
def post_save_product_batch(**kwargs):
    product_batch = kwargs['instance']
    product = product_batch.product

    product.amount = F('amount') + product_batch.amount
    product.save(update_fields=['amount'])


@receiver(pre_delete, sender=Product)
def pre_delete_product(**kwargs):
    delete_all_photo(**kwargs)


@receiver(pre_delete, sender=Category)
def pre_delete_category(**kwargs):
    delete_all_photo(**kwargs)


def delete_all_photo(**kwargs):
    instance = kwargs['instance']
    instance.delete_all_instance_photos()
