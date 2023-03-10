from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class AdminUser(UserAdmin):

    list_display = ('username', 'is_active', 'date_joined', 'orders',
                    'orders_amount')
    list_display_links = ('username', 'date_joined', 'orders',
                          'orders_amount')
    list_editable = ('is_active',)

    def delete_queryset(self, request, queryset):
        for i in queryset:
            i.delete()


admin.site.register(User, AdminUser)
