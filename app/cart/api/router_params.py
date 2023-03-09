from api.services.router import RouterRegisterParams
from .views import CartViewSet

cart_router_params = RouterRegisterParams(
    prefix=r'cart', viewset=CartViewSet, basename='cart')._asdict()
