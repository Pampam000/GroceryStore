from rest_framework.serializers import ModelSerializer

from ..models import Product, Category, Producer, ProductBatch


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ('pk', 'name', 'producer', 'weight', 'measure', 'photo',
                  'category', 'amount', 'price', 'is_available', 'description',
                  'discount_size', 'store_conditions', 'energy_value', 'slug')
        read_only_fields = ('slug',)


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ('pk', 'name', 'photo', 'slug')
        read_only_fields = ('slug',)


class ProducerSerializer(ModelSerializer):
    class Meta:
        model = Producer
        fields = ('pk', 'name', 'country')


class ProductBatchSerializer(ModelSerializer):
    class Meta:
        model = ProductBatch
        fields = ('product', 'amount', 'purchase_price', 'packing_date',
                  'sell_before')
        read_only_fields = ('time_created',)
