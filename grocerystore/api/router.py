from rest_framework.routers import DefaultRouter

from applications.store.api.router_params import category_router_params, \
    producer_router_params, product_router_params, product_batch_router_params
from applications.cart.api.router_params import cart_router_params
from applications.orders.api.router_params import order_router_params, \
    order_item_router_params
from applications.users.api.router_params import user_router_params

router = DefaultRouter()

router.register(**category_router_params)
router.register(**producer_router_params)
router.register(**product_router_params)
router.register(**product_batch_router_params)

router.register(**cart_router_params)

router.register(**order_router_params)
router.register(**order_item_router_params)

router.register(**user_router_params)