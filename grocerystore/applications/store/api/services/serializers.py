from applications.store.models import Product


class ProductMeta:
    model = Product
    fields = ('pk', 'name', 'producer', 'weight', 'measure', 'photo',
              'category', 'amount', 'price', 'is_available', 'description',
              'discount_size', 'min_temperature', 'max_temperature',
              'energy_value', 'discount_price', 'slug')
    read_only_fields = ('slug',)
