from api.services.router import RouterRegisterParams
from .views import UserViewSet

user_router_params = RouterRegisterParams(
    prefix=r'users', viewset=UserViewSet, basename='users'). \
    _asdict()
