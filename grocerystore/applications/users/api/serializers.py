from rest_framework.serializers import ModelSerializer

from ..models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'is_active', 'date_joined',
                  'get_orders', 'orders_amount')
        read_only_fields = ('date_joined',)
