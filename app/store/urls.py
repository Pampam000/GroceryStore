from django.urls import path

from . import views as v

urlpatterns = [
    path('', v.index, name='home'),
    path('categories/<slug:name>/', v.show_products_in_category,
         name='products_in_category'),
    path('products/<slug:name>/', v.show_product_info, name='product')

]
