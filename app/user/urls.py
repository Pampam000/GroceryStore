from django.urls import path

from . import views as v
from .services import config

urlpatterns = [
    path(config.SIGNUP_URL, v.CreateUser.as_view(), name='sign-up'),
    path(config.LOGIN_URL, v.LogIn.as_view(), name='log-in'),
    path(config.LOGOUT_URL, v.LogOut.as_view(), name='log-out')
]
