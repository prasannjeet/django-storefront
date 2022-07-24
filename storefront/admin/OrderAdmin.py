from django.contrib import admin

from storefront.admin.util.OrderItemInline import OrderItemInline
from storefront.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    inlines = [OrderItemInline]

    list_display: tuple[str, str, str, str] = ('id', 'placed_at', 'payment_status', 'customer')
    list_editable: tuple[str] = ('payment_status',)
    list_select_related: list[str] = ['customer']
    list_per_page: int = 10