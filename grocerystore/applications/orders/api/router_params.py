from api.services.router import RouterRegisterParams
from .views import OrderViewSet, OrderItemViewSet, AdminOrderViewSet

admin_order_router_params = RouterRegisterParams(
    prefix=r'orders-admin', viewset=AdminOrderViewSet, basename='order-admin'
)._asdict()

order_router_params = RouterRegisterParams(
    prefix=r'orders', viewset=OrderViewSet, basename='order')._asdict()

order_item_router_params = RouterRegisterParams(
    prefix=r'order-items', viewset=OrderItemViewSet, basename='order-item'). \
    _asdict()
