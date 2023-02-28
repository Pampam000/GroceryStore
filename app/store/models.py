import decimal as d
import json
from datetime import datetime, timedelta

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models as m
from django.urls import reverse

from .services import models as md


class Category(md.PhotoAbstractModel):
    class Meta:
        verbose_name_plural = 'Categories'

    name = m.CharField(unique=True, max_length=50)
    slug = m.SlugField(max_length=100, db_index=True)
    photo = m.ImageField(upload_to=md.get_photo_path_for_category)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('store:products_in_category',
                       kwargs={'category_slug': self.slug})


class Producer(m.Model):
    name = m.CharField(primary_key=True, max_length=50)
    country = m.CharField(max_length=20)

    def __str__(self):
        return self.name


class Product(md.PhotoAbstractModel):
    class Meta:
        unique_together = ('name', 'weight', 'measure', 'producer')

    CHOICES = (
        (None, 'Measure not chosen'),
        ('kg', 'Kg'),
        ('g', 'g'),
        ('l', 'L'),
        ('ml', 'mL')
    )

    name = m.CharField(max_length=50)
    producer = m.ForeignKey('Producer', on_delete=m.PROTECT,
                            default='Producer1')
    weight = m.DecimalField(default=1, max_digits=4, decimal_places=2,
                            validators=[MinValueValidator(limit_value=1)],
                            verbose_name='volume/weight')
    measure = m.CharField(max_length=5, choices=CHOICES)
    slug = m.SlugField(max_length=100, db_index=True)
    amount = m.PositiveSmallIntegerField(default=0)
    price = m.DecimalField(
        default=20, max_digits=5, decimal_places=2,
        validators=[MinValueValidator(limit_value=1)])

    photo = m.ImageField(upload_to=md.get_photo_path_for_product)

    is_available = m.BooleanField(default=True, auto_created=True,
                                  verbose_name='available')

    category = m.ForeignKey('Category', on_delete=m.PROTECT,
                            default='Category1')

    description = m.TextField(null=True, blank=True)
    discount_size = m.PositiveSmallIntegerField(
        validators=[MaxValueValidator(limit_value=99)], default=10,
        verbose_name='discount')

    calories = m.PositiveSmallIntegerField(**md.params)
    proteins = m.PositiveSmallIntegerField(**md.params)
    fats = m.PositiveSmallIntegerField(**md.params)
    carbohydrates = m.PositiveSmallIntegerField(**md.params)

    min_temperature = m.SmallIntegerField(default=-5)
    max_temperature = m.SmallIntegerField(default=+8)

    def __str__(self):
        return f"{self.name} {self.producer.name} {float(self.weight)} " \
               f"{self.measure}"

    def get_absolute_url(self):
        return reverse('store:product', kwargs={'name': self.slug})

    def store_conditions(self) -> str:
        return '{} to {}'.format(
            self.__check_temperature_sign(self.min_temperature),
            self.__check_temperature_sign(self.max_temperature))

    def get_discount_price(self) -> d.Decimal:
        return (self.price * d.Decimal(str(1 - self.discount_size / 100))). \
            quantize(d.Decimal('1.00'), d.ROUND_HALF_UP)

    def as_cart_item(self):
        return json.dumps(
            {self.slug: {
                "Image": self.get_extra_small_photo(),
                "Product": str(self),
                "Price": str(self.price),
                "Discount price": str(self.get_discount_price())}})

    def get_energy_value(self) -> dict:
        return {
            "Kcal": self.calories,
            "Proteins": self.proteins,
            "Fats": self.fats,
            "Carbs": self.carbohydrates
        }

    def get_detail_info(self) -> dict:
        return {
            "Producer": f"{self.producer}, {self.producer.country}",
            "Store at": self.store_conditions(),
            "Discount": f"{self.discount_size} %",
            "Price": f"{self.price} $",
            "Discount price": f"{self.get_discount_price()} $"
        }

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

    def __str__(self):
        return str(self.product)
