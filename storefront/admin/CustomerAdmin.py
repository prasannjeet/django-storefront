from django.contrib import admin
from django.db.models import QuerySet, Count
from django.http import HttpRequest
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode

from storefront.models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display: tuple[str, str, str, str] = ('name', 'email', 'membership', 'orders_count')
    list_editable: tuple[str] = ('membership',)
    list_per_page: int = 10
    ordering: list[str] = ['last_name', 'first_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith', 'email__istartswith']

    # Order by first and last name
    @admin.display(ordering='first_name')
    def name(self, customer) -> str:
        return f'{customer.first_name} {customer.last_name}'

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).annotate(
            orders_count=Count('order')
        )

    @admin.display(ordering='orders_count')
    def orders_count(self, customer) -> int:
        url = (
                reverse('admin:storefront_order_changelist')
                + '?'
                + urlencode({
                    'customer__id': str(customer.id)
                })
        )
        return format_html('<a href="{}">{}</a>', url, customer.orders_count)

    orders_count.short_description = 'Number of orders'
