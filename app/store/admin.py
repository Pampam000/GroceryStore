from django.contrib import admin as a

from .models import Product, Producer, Category, ProductBatch


class ProductAdmin(a.ModelAdmin):
    list_display = ('name', 'producer', 'weight', 'measure', 'price',
                    'is_available', 'amount')
    search_fields = ('name', 'category__name')
    list_editable = ('is_available',)
    list_filter = ('name', 'price', 'is_available')
    prepopulated_fields = {'slug': ('name', 'producer', 'weight', 'measure')}


class CategoryAdmin(a.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class ProducerAdmin(a.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


a.site.register(Product, ProductAdmin)
a.site.register(Producer, ProducerAdmin)
a.site.register(Category, CategoryAdmin)
a.site.register(ProductBatch)
