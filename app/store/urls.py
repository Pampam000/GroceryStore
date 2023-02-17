from django.urls import path

from . import views as v


urlpatterns = [
    path('', v.CategoryListView.as_view(), name='home'),
    path('categories/<slug:category_slug>/', v.ProductListView.as_view(),
         name='products_in_category'),
    path('products/<slug:name>/', v.ProductDetail.as_view(), name='product'),

]
