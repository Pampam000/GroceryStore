from django.db.models import F
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.utils.text import slugify

from .models import ProductBatch, Product, Category


@receiver(post_save, sender=ProductBatch)
def post_save_product_batch(**kwargs):
    product_batch = kwargs['instance']
    product = product_batch.product

    product.amount = F('amount') + product_batch.amount
    product.save(update_fields=['amount'])


@receiver(post_delete, sender=Product)
def post_delete_product(**kwargs):
    delete_all_photo(**kwargs)


@receiver(post_delete, sender=Category)
def post_delete_category(**kwargs):
    delete_all_photo(**kwargs)


@receiver(pre_save, sender=Product)
def create_slug_for_product(**kwargs):
    create_slug(**kwargs)


@receiver(pre_save, sender=Category)
def create_slug_for_category(**kwargs):
    instance = kwargs['instance']
    instance.slug = slugify(instance)


def delete_all_photo(**kwargs):
    instance = kwargs['instance']
    instance.delete_all_instance_photos()


def create_slug(**kwargs):
    instance = kwargs['instance']

    if not instance.pk:  # If instance is not created yet
        instance.slug = slugify(instance)
