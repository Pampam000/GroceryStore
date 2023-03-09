from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('product', 'price', 'discount_price', 'quantity',
                       'total_price')
    can_delete = False
    max_num = 1
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderItemInline,)
    readonly_fields = ('price', 'user', 'address')

    list_select_related = True
    list_display = ('id', 'user', 'is_user_active', 'address', 'is_paid',
                    'unique_products_count', 'total_products_amount', 'price',
                    'created_at')
    list_display_links = ('id', 'price', 'created_at')
    list_editable = ('is_paid',)

    search_fields = ('id', 'user__username', 'address', 'created_at')
    search_help_text = "Searching at order id, address, users or created time"
    show_full_result_count = False

    list_filter = ('user__username', 'address')


class OrderItemAdmin(admin.ModelAdmin):
    list_select_related = True
    list_display = ('order', 'product', 'price', 'discount_price', 'quantity',
                    'total_price')
    search_fields = ('order__id', 'product__name')
    search_help_text = "Searching at order id and product"


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
