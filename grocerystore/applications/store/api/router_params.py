from api.services.router import RouterRegisterParams
from .views import CategoryViewSet, ProductViewSet, ProducerViewSet

category_router_params = RouterRegisterParams(
    prefix=r'categories', viewset=CategoryViewSet, basename='category'). \
    _asdict()

producer_router_params = RouterRegisterParams(
    prefix=r'producers', viewset=ProducerViewSet, basename='producer'). \
    _asdict()

product_router_params = RouterRegisterParams(
    prefix=r'products', viewset=ProductViewSet, basename='product'). \
    _asdict()

product_batch_router_params = RouterRegisterParams(
    prefix=r'product-batches', viewset=CategoryViewSet,
    basename='product-batch')._asdict()
