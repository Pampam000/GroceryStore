from datetime import datetime, timedelta

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models as m
from django.urls import reverse

from .services import models as md


class Product(md.InstanceImage, m.Model):
    name = m.CharField(max_length=50)
    price = m.DecimalField(default=20, decimal_places=2, max_digits=5,
                           validators=[MinValueValidator(limit_value=1)])
    amount = m.PositiveIntegerField(default=100)
    photo = m.ImageField(upload_to=md.get_photo_path_for_product)
    time_created = m.DateTimeField(auto_now_add=True)
    is_available = m.BooleanField(default=True, auto_created=True)
    producer = m.ForeignKey('Producer', on_delete=m.PROTECT,
                            related_name='producers_products')
    category = m.ForeignKey('Category', on_delete=m.PROTECT,
                            related_name='category_products')

    description = m.TextField(null=True, blank=True)
    discount_size = m.PositiveSmallIntegerField(
        validators=[MaxValueValidator(limit_value=99)], default=0)

    calories = m.PositiveSmallIntegerField(**md.params)
    proteins = m.PositiveSmallIntegerField(**md.params)
    fats = m.PositiveSmallIntegerField(**md.params)
    carbohydrates = m.PositiveSmallIntegerField(**md.params)

    packing_date = m.DateTimeField(default=datetime.now() -
                                           timedelta(hours=4))
    sell_before = m.DateTimeField(default=datetime.now()
                                          + timedelta(days=7))
    min_temperature = m.SmallIntegerField(default=-5)
    max_temperature = m.SmallIntegerField(default=+8)

    def get_absolute_url(self):
        return reverse('product', kwargs={'name': self.name})

    def store_conditions(self) -> str:
        min_t = self.__check_temperature_sign(self.min_temperature)
        max_t = self.__check_temperature_sign(self.max_temperature)
        return f'{min_t} to {max_t}'

    def total_price(self):
        return round(float(self.price) * (1 - self.discount_size / 100), 2)

    @property
    def is_new(self):
        return (datetime.now() - self.time_created.replace(tzinfo=None)
                ).days <= 14

    @property
    def is_close_to_expire(self):
        return (self.sell_before.replace(tzinfo=None) - datetime.now()
                ).days < 2

    @property
    def is_expired(self):
        return datetime.now() >= self.sell_before.replace(tzinfo=None)

    def __str__(self):
        return self.name

    @staticmethod
    def __check_temperature_sign(temp: int) -> str:
        str_temp = f"{temp}°C"
        return f'+{str_temp}' if temp > 0 else str_temp


class Category(md.InstanceImage, m.Model):
    name = m.CharField(unique=True, max_length=50)
    photo = m.ImageField(upload_to=md.get_photo_path_for_category)

    class Meta:
        verbose_name_plural = 'Categories'

    def get_absolute_url(self):
        return reverse('products_in_category', kwargs={'name': self.name})

    def __str__(self):
        return self.name


class Producer(m.Model):
    name = m.CharField(unique=True, max_length=50)
    country = m.CharField(max_length=20)

    def __str__(self):
        return self.name
