from django.contrib import admin

from .models import Product, Producer, Category


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'price', 'is_close_to_expire',
                    'is_expired', 'sell_before', 'is_available')
    search_fields = ('name', 'category__name')
    list_editable = ('is_available',)
    list_filter = ('name', 'price', 'is_available', 'sell_before')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class ProducerAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Producer, ProducerAdmin)
admin.site.register(Category, CategoryAdmin)