from datetime import datetime, timedelta

from django.core.validators import MaxValueValidator
from django.db import models as m

null = {'null': True, 'blank': True}
params = {'validators': [MaxValueValidator(limit_value=999)],
          'help_text': 'per_100_grams'} | null


class Product(m.Model):
    name = m.CharField(max_length=50)
    price = m.PositiveIntegerField(default=200)
    amount = m.PositiveIntegerField()
    photo = m.ImageField(upload_to="photos/%Y/%m/%d/")
    time_created = m.DateTimeField(auto_now_add=True)
    is_available = m.BooleanField(default=True, auto_created=True)
    producer = m.ForeignKey('Producer', on_delete=m.PROTECT,
                            related_name='producers_products')
    category = m.ForeignKey('Category', on_delete=m.PROTECT,
                            related_name='category_products')

    description = m.TextField(**null)
    discount_size = m.PositiveSmallIntegerField(
        validators=[MaxValueValidator(limit_value=99)], default=0)

    calories = m.PositiveSmallIntegerField(**params)
    proteins = m.PositiveSmallIntegerField(**params)
    fats = m.PositiveSmallIntegerField(**params)
    carbohydrates = m.PositiveSmallIntegerField(**params)

    packing_date = m.DateTimeField(default=datetime.now() -
                                           timedelta(hours=4))
    sell_before = m.DateTimeField(default=datetime.now()
                                          + timedelta(days=7))
    min_temperature = m.SmallIntegerField(**null)
    max_temperature = m.SmallIntegerField(**null)

    @property
    def is_new(self):
        return (datetime.now() - self.time_created.replace(tzinfo=None)
                ).days <= 14

    @property
    def is_close_to_expire(self):
        print((self.sell_before.replace(tzinfo=None) - datetime.now()
               ).days)
        return (self.sell_before.replace(tzinfo=None) - datetime.now()
                ).days < 2

    @property
    def is_expired(self):
        print(self.sell_before)
        return datetime.now() >= self.sell_before.replace(tzinfo=None)

    def __str__(self):
        return self.name


class Category(m.Model):
    name = m.CharField(unique=True, max_length=50)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Producer(m.Model):
    name = m.CharField(unique=True, max_length=50)
    country = m.CharField(max_length=20)

    def __str__(self):
        return self.name

