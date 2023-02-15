from django.urls import re_path, path

from . import views as v

urlpatterns = [
    re_path(r'^create/$', v.OrderCreateView.as_view(), name='order_create'),
    path('order-successfully-created/<slug:order>/', v.success, name='success')

]

