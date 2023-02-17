from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ('pk', 'user', 'address', 'is_paid')


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('pk', 'order', 'quantity', 'get_product_total_price', 'get_cost')

admin.site.register(Order, OrderAdmin)

admin.site.register(OrderItem, OrderItemAdmin)