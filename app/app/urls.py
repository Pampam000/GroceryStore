"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from .api_router import router
from . import settings as st
# necessary imports for api
from cart.api import routers
from orders.api import routers
from store.api import routers

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^cart/', include('cart.urls')),
    re_path(r'^orders/',
            include(('orders.urls', 'orders'), namespace='orders')),
    path('', include(('store.urls', 'store'), namespace='store')),
    path('', include('user.urls')),

    path('api/v1/',include(router.urls)),

]


if st.DEBUG:
    urlpatterns.insert(0, path('__debug__/', include('debug_toolbar.urls')))
    urlpatterns += static(st.MEDIA_URL, document_root=st.MEDIA_ROOT)
