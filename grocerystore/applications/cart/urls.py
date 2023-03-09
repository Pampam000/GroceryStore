from django.urls import re_path, path

from . import views as v

urlpatterns = [
    re_path(r'^$', v.CartDetailView.as_view(), name='cart_detail'),
    path('add/', v.CartAddItemView.as_view(),
         name='cart_add'),
    path('remove/<slug:product_slug>/', v.CartRemoveItemView.as_view(),
         name='cart_remove'),
]
