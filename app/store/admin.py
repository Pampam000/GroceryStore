from django.contrib import admin

from .models import Product, Producer, Category, ProductBatch


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'producer', 'weight', 'measure', 'price',
                    'is_available', 'amount')
    search_fields = ('name', 'category__name')
    list_editable = ('is_available',)
    list_filter = ('name', 'price', 'is_available')
    prepopulated_fields = {'slug': ('name', 'producer', 'weight', 'measure')}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class ProducerAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Producer, ProducerAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductBatch)
