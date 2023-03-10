from rest_framework.serializers import ModelSerializer

from .services.serializers import ProductMeta
from ..models import Category, Producer, ProductBatch


class ProductSerializer(ModelSerializer):
    class Meta(ProductMeta):
        pass


class ProductSerializerWithDepth(ProductSerializer):
    class Meta(ProductMeta):
        depth = 1


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
