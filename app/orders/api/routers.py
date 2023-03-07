from app.api_router import router
from .views import OrderViewSet, OrderItemViewSet

router.register(r'orders', OrderViewSet, basename='order')
router.register(r'order-items', OrderItemViewSet, basename='order-item')
