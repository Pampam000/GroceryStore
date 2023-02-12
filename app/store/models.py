from datetime import datetime, timedelta

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models as m
from django.urls import reverse

from .services import models as md


class Category(md.InstanceImage, m.Model):
    class Meta:
        verbose_name_plural = 'Categories'

    name = m.CharField(primary_key=True, max_length=50)
    slug = m.SlugField(max_length=100, db_index=True, verbose_name="URL")
    photo = m.ImageField(upload_to=md.get_photo_path_for_category)

    def get_absolute_url(self):
        return reverse('products_in_category',
                       kwargs={'category_slug': self.slug})

    def __str__(self):
        return self.name


class Producer(m.Model):
    name = m.CharField(primary_key=True, max_length=50)
    country = m.CharField(max_length=20)

    def __str__(self):
        return self.name


class Product(md.InstanceImage, m.Model):
    class Meta:
        unique_together = ('name', 'weight', 'measure', 'producer')

    class Measure(m.TextChoices):
        kg = 'kg', 'kg'
        g = 'g', 'g'
        l = 'l', 'l'
        ml = 'ml', 'ml'

    name = m.CharField(max_length=50)
    producer = m.ForeignKey('Producer', on_delete=m.PROTECT)
    weight = m.DecimalField(default=1, max_digits=4, decimal_places=2,
                            validators=[MinValueValidator(limit_value=1)],
                            verbose_name='volume/weight')
    measure = m.CharField(max_length=5, choices=Measure.choices)
    slug = m.SlugField(max_length=100, db_index=True,  verbose_name="URL")
    amount = m.PositiveSmallIntegerField(default=0)
    price = m.DecimalField(
        default=20, max_digits=5, decimal_places=2,
        validators=[MinValueValidator(limit_value=1)])

    photo = m.ImageField(upload_to=md.get_photo_path_for_product)

    is_available = m.BooleanField(default=True, auto_created=True)

    category = m.ForeignKey('Category', on_delete=m.PROTECT)

    description = m.TextField(null=True, blank=True)
    discount_size = m.PositiveSmallIntegerField(
        validators=[MaxValueValidator(limit_value=99)], default=0)

    calories = m.PositiveSmallIntegerField(**md.params)
    proteins = m.PositiveSmallIntegerField(**md.params)
    fats = m.PositiveSmallIntegerField(**md.params)
    carbohydrates = m.PositiveSmallIntegerField(**md.params)

    min_temperature = m.SmallIntegerField(default=-5)
    max_temperature = m.SmallIntegerField(default=+8)

    def get_absolute_url(self):
        return reverse('product', kwargs={'name': self.slug})

    def store_conditions(self) -> str:
        min_t = self.__check_temperature_sign(self.min_temperature)
        max_t = self.__check_temperature_sign(self.max_temperature)
        return f'{min_t} to {max_t}'

    def total_price(self):
        return round(float(self.price) * (1 - self.discount_size / 100), 2)

    def __str__(self):
        return f"{self.name} {self.producer.name} {float(self.weight)} " \
               f"{self.measure}"

    @staticmethod
    def __check_temperature_sign(temp: int) -> str:
        str_temp = f"{temp}°C"
        return f'+{str_temp}' if temp > 0 else str_temp


class ProductBatch(m.Model):
    class Meta:
        verbose_name_plural = 'Product Batches'

    product = m.ForeignKey('Product', on_delete=m.PROTECT)
    amount = m.PositiveIntegerField(default=100)
    purchase_price = m.DecimalField(
        default=10, decimal_places=2, max_digits=5,
        validators=[MinValueValidator(limit_value=1)])
    time_created = m.DateTimeField(auto_now_add=True)
    packing_date = m.DateTimeField(default=datetime.now() - timedelta(hours=4))
    sell_before = m.DateTimeField(default=datetime.now() + timedelta(days=7))

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.product.amount += self.amount
        self.product.save()

    def __str__(self):
        return self.product.__str__()
