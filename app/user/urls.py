from django.urls import path

from . import views as v

urlpatterns = [
    path('sign-up/', v.CreateUser.as_view(), name='sign-up'),
    path('log-in/', v.LogIn.as_view(), name='log-in'),
    path('log-out/', v.log_out, name='log-out')
]
