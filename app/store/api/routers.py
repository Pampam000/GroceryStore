from app.api_router import router
from .views import CategoryViewSet, ProductViewSet, ProductBatchViewSet, \
    ProducerViewSet

router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'product-batches', ProductBatchViewSet,
                basename='product-batch')
router.register(r'producers', ProducerViewSet, basename='producer')
