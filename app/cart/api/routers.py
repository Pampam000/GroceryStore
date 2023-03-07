from app.api_router import router
from .views import CartViewSet

router.register(r'cart', CartViewSet, basename='cart')
