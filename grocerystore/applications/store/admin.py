from django.contrib import admin as a

from .models import Product, Producer, Category, ProductBatch


class ProductAdmin(a.ModelAdmin):
    list_display = ('name', 'producer', 'weight', 'measure', 'price',
                    'is_available', 'amount')
    search_fields = ('name', 'category__name', 'producer__name')
    list_editable = ('is_available', 'amount', 'price', 'weight', 'measure',
                     'producer')
    list_filter = ('name', 'price', 'is_available')
    fields = (
        ('name', 'producer', 'category'),
        ('weight', 'measure'),
        ('amount', 'price', 'discount_size'),
        'photo',
        ('calories', 'proteins', 'fats', 'carbohydrates'),
        ('min_temperature', 'max_temperature'),
        'slug'
    )
    readonly_fields = ('slug',)


class CategoryAdmin(a.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)
    readonly_fields = ('slug',)


class ProducerAdmin(a.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


a.site.register(Product, ProductAdmin)
a.site.register(Producer, ProducerAdmin)
a.site.register(Category, CategoryAdmin)
a.site.register(ProductBatch)
